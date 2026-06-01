"""Config-driven polite scraper.

Reads config/sources.yaml; for each source crawls the listed sublinks, follows
in-page article links, downloads the article body + main image, and emits one
JSONL row per article to data/raw/scraped.jsonl. Honours robots.txt + per-host
rate limit; caches HTML on disk under data/raw/html_cache/.
"""
from __future__ import annotations

import argparse
import hashlib
import time
import urllib.parse
import urllib.robotparser
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from src.utils import append_jsonl, ensure_dir, get_logger, read_yaml

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"
DEFAULT_SOURCES = PROJECT_ROOT / "config" / "sources.yaml"


def _stable_id(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def _cache_path(cache_dir: Path, url: str) -> Path:
    return cache_dir / f"{_stable_id(url)}.html"


def _robots_for(base_url: str) -> urllib.robotparser.RobotFileParser:
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(base_url, "/robots.txt"))
    try:
        rp.read()
    except Exception as e:
        log.warning("robots.txt fetch failed for %s: %s (assuming allow)", base_url, e)
    return rp


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def _fetch(url: str, ua: str, timeout: int) -> requests.Response:
    return requests.get(url, headers={"User-Agent": ua}, timeout=timeout)


def _extract_article(html: str, source_selectors: dict | None = None) -> dict:
    """Generic readability-ish extraction: og:title, og:image, main <article> text."""
    soup = BeautifulSoup(html, "lxml")
    sel = source_selectors or {}

    title_tag = soup.find("meta", property="og:title")
    title = title_tag["content"].strip() if title_tag and title_tag.get("content") else ""
    if not title and soup.title:
        title = soup.title.get_text(strip=True)

    img_tag = soup.find("meta", property="og:image")
    image_url = img_tag["content"].strip() if img_tag and img_tag.get("content") else ""

    if "image" in sel:
        node = soup.select_one(sel["image"])
        if node and node.get("src"):
            image_url = node["src"]

    body_node = None
    if "article" in sel:
        body_node = soup.select_one(sel["article"])
    if body_node is None:
        body_node = soup.find("article") or soup.find("main") or soup.body
    paragraphs = []
    if body_node is not None:
        for p in body_node.find_all("p"):
            txt = p.get_text(" ", strip=True)
            if txt:
                paragraphs.append(txt)
    text = "\n\n".join(paragraphs)
    return {"title": title, "text": text, "image_url": image_url}


def _is_article_link(url: str, base: str) -> bool:
    if not url:
        return False
    if url.startswith("javascript:") or url.startswith("mailto:"):
        return False
    abs_url = urllib.parse.urljoin(base, url)
    return urllib.parse.urlparse(abs_url).netloc == urllib.parse.urlparse(base).netloc


def _discover_links(html: str, base: str, link_pattern: str | None = None) -> list[str]:
    import re as _re
    pat = _re.compile(link_pattern) if link_pattern else None
    soup = BeautifulSoup(html, "lxml")
    out: list[str] = []
    seen: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not _is_article_link(href, base):
            continue
        abs_url = urllib.parse.urljoin(base, href).split("#", 1)[0]
        if abs_url in seen:
            continue
        if pat and not pat.search(abs_url):
            continue
        seen.add(abs_url)
        out.append(abs_url)
    return out


def _download_image(image_url: str, source_name: str, images_dir: Path, ua: str, timeout: int) -> str | None:
    if not image_url:
        return None
    try:
        r = requests.get(image_url, headers={"User-Agent": ua}, timeout=timeout, stream=True)
        r.raise_for_status()
        ext = ".jpg"
        ct = r.headers.get("content-type", "").lower()
        if "png" in ct:
            ext = ".png"
        elif "webp" in ct:
            ext = ".webp"
        h = hashlib.sha1(image_url.encode("utf-8")).hexdigest()[:16]
        out_dir = ensure_dir(images_dir / source_name)
        path = out_dir / f"{h}{ext}"
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
        return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
    except Exception as e:
        log.warning("image download failed (%s): %s", image_url, e)
        return None


def crawl_source(
    source_cfg: dict,
    scraper_cfg: dict,
    raw_dir: Path,
    out_jsonl: Path,
    limit: int | None = None,
    dry_run: bool = False,
) -> int:
    name = source_cfg["name"]
    base = source_cfg["base_url"]
    src_type = source_cfg.get("source_type", "unknown")
    rate = float(source_cfg.get("rate_limit_s", scraper_cfg.get("rate_limit_s", 1.5)))
    timeout = int(scraper_cfg.get("timeout_s", 20))
    ua = scraper_cfg.get("user_agent", "DecodingDeceptionResearchBot/0.1")

    if "placeholder" in name.lower() or "example" in base.lower():
        log.warning("Source %s looks like a placeholder; skipping. Edit config/sources.yaml.", name)
        return 0

    robots = _robots_for(base) if source_cfg.get("robots_respect", True) else None
    cache_dir = ensure_dir(raw_dir / "html_cache" / name)
    images_dir = ensure_dir(raw_dir / "images")

    # Expand {pageNumber} in sublinks against page_range, if any.
    raw_sublinks = list(source_cfg.get("sublinks", []))
    pr = source_cfg.get("page_range")
    expanded: list[str] = []
    for sublink in raw_sublinks:
        if "{pageNumber}" in sublink:
            if not pr:
                log.warning("%s has {pageNumber} but no page_range; using page 1 only", sublink)
                expanded.append(sublink.replace("{pageNumber}", "1"))
            else:
                start, end = int(pr[0]), int(pr[1])
                for n in range(start, end + 1):
                    expanded.append(sublink.replace("{pageNumber}", str(n)))
        else:
            expanded.append(sublink)

    discovered: list[str] = []
    for sublink in expanded:
        if robots and not robots.can_fetch(ua, sublink):
            log.warning("robots.txt disallows %s, skipping", sublink)
            continue
        try:
            resp = _fetch(sublink, ua, timeout)
            time.sleep(rate)
            if resp.status_code != 200:
                log.warning("seed %s -> HTTP %d", sublink, resp.status_code)
                continue
            links = _discover_links(resp.text, base, source_cfg.get("article_link_pattern"))
            discovered.extend(links)
            log.info("seed %s -> %d candidate links", sublink, len(links))
        except Exception as e:
            log.warning("seed fetch failed (%s): %s", sublink, e)

    # Dedup, cap, and respect max_articles.
    seen, queue = set(), []
    for u in discovered:
        if u in seen:
            continue
        seen.add(u)
        queue.append(u)
    cap = limit if limit is not None else source_cfg.get("max_articles")
    if cap:
        queue = queue[: int(cap)]

    n_written = 0
    for url in queue:
        if robots and not robots.can_fetch(ua, url):
            continue
        try:
            cp = _cache_path(cache_dir, url)
            if cp.exists() and scraper_cfg.get("cache_html", True):
                html = cp.read_text(encoding="utf-8", errors="ignore")
            else:
                resp = _fetch(url, ua, timeout)
                time.sleep(rate)
                if resp.status_code != 200:
                    continue
                html = resp.text
                if scraper_cfg.get("cache_html", True):
                    cp.write_text(html, encoding="utf-8")
            sel = source_cfg.get("selectors") or {}
            parsed = _extract_article(html, sel)
            if not parsed["text"] or len(parsed["text"].split()) < 50:
                continue  # too short to be a real article
            if dry_run:
                log.info("[dry-run] %s -> %d chars", url, len(parsed["text"]))
                continue
            image_rel = _download_image(parsed["image_url"], name, images_dir, ua, timeout)
            row = {
                "id": f"scraped:{name}:{_stable_id(url)}",
                "url": url,
                "source": name,
                "source_type": src_type,
                "title": parsed["title"],
                "text": parsed["text"],
                "image_path": image_rel,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }
            append_jsonl(out_jsonl, row)
            n_written += 1
        except Exception as e:
            log.warning("article failed (%s): %s", url, e)
    log.info("source %s: wrote %d articles", name, n_written)
    return n_written


def main() -> None:
    parser = argparse.ArgumentParser(description="Polite multi-source scraper.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--sources", default=str(DEFAULT_SOURCES))
    parser.add_argument("--limit", type=int, default=None, help="Cap articles per source")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", default=None, help="Only run this source name")
    args = parser.parse_args()

    cfg = read_yaml(args.config)
    sources_cfg = read_yaml(args.sources)
    raw_dir = ensure_dir(PROJECT_ROOT / cfg["paths"]["raw_dir"])
    out_jsonl = raw_dir / "scraped.jsonl"
    if not args.dry_run and out_jsonl.exists():
        log.info("Appending to existing %s (truncate manually for a fresh run)", out_jsonl)

    sources: Iterable[dict] = sources_cfg.get("sources", [])
    total = 0
    for s in sources:
        if args.only and s["name"] != args.only:
            continue
        total += crawl_source(s, cfg["scraper"], raw_dir, out_jsonl, args.limit, args.dry_run)
    log.info("DONE. Total written: %d", total)


if __name__ == "__main__":
    main()
