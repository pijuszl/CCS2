"""Fetch the main image for each LITUND article using its native `Nuoroda` URL.

LITUND ships article URLs in its metadata files. Since each article already has
a ground-truth label from the corpus structure (LRT subset -> non, Unreliable
subset -> hidden), no LLM labelling is needed for these images — they inherit
their parent article's label.

Writes:
  data/raw/images/litund/{subset}/{failas}.{jpg|png|webp}
  data/raw/litund_images.jsonl   (one row per successful fetch)
"""
from __future__ import annotations

import argparse
import hashlib
import time
import urllib.parse
import urllib.robotparser
from collections import defaultdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from src.data.load_existing import _read_litund_metadata
from src.utils import append_jsonl, ensure_dir, get_logger, read_yaml

log = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def _fetch(url: str, ua: str, timeout: int) -> requests.Response:
    return requests.get(url, headers={"User-Agent": ua}, timeout=timeout, allow_redirects=True)


def _extract_image_url(html: str) -> str | None:
    soup = BeautifulSoup(html, "lxml")
    tag = soup.find("meta", property="og:image")
    if tag and tag.get("content"):
        return tag["content"].strip()
    tag = soup.find("meta", attrs={"name": "twitter:image"})
    if tag and tag.get("content"):
        return tag["content"].strip()
    art = soup.find("article") or soup.find("main") or soup.body
    if art:
        img = art.find("img", src=True)
        if img and img.get("src"):
            return img["src"]
    return None


def _download_image(image_url: str, dst_base: Path, ua: str, timeout: int) -> str | None:
    try:
        r = requests.get(image_url, headers={"User-Agent": ua}, timeout=timeout,
                         stream=True, allow_redirects=True)
        r.raise_for_status()
        ct = r.headers.get("content-type", "").lower()
        ext = ".jpg"
        if "png" in ct:
            ext = ".png"
        elif "webp" in ct:
            ext = ".webp"
        elif "gif" in ct:
            ext = ".gif"
        dst = dst_base.with_suffix(ext)
        ensure_dir(dst.parent)
        with open(dst, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
        return str(dst.relative_to(PROJECT_ROOT)).replace("\\", "/")
    except Exception as e:
        log.warning("image download failed (%s): %s", image_url, e)
        return None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=str(DEFAULT_CONFIG))
    p.add_argument("--limit", type=int, default=None, help="Cap total URLs")
    p.add_argument("--rate-limit-s", type=float, default=1.5,
                   help="Min seconds between requests to the SAME host")
    p.add_argument("--timeout-s", type=int, default=20)
    p.add_argument("--only-subset", choices=["unreliable", "lrt"], default=None)
    args = p.parse_args()

    cfg = read_yaml(args.config)
    ua = cfg["scraper"].get("user_agent", "DecodingDeceptionResearchBot/0.1")
    datasets_dir = PROJECT_ROOT / cfg["paths"]["datasets_dir"]
    raw_dir = ensure_dir(PROJECT_ROOT / cfg["paths"]["raw_dir"])
    out_jsonl = raw_dir / "litund_images.jsonl"
    images_root = ensure_dir(raw_dir / "images" / "litund")
    cache_root = ensure_dir(raw_dir / "html_cache" / "litund")

    # Build the queue from both LITUND metadata files
    queue: list[dict] = []
    for subset, meta_name, src_type in [
        ("unreliable", "unreliable_corpus-metadata.txt", "propaganda"),
        ("lrt", "LRT_corpus-metadata.txt", "neutral"),
    ]:
        if args.only_subset and args.only_subset != subset:
            continue
        meta_path = datasets_dir / "LITUND" / meta_name
        if not meta_path.exists():
            log.warning("missing %s, skipping", meta_path)
            continue
        df = _read_litund_metadata(meta_path)
        # Find URL column (Nuoroda). Skip Paneigimo_nuoroda which is the
        # fact-check rebuttal URL, not the article itself.
        url_col = None
        for c in df.columns:
            cl = c.lower()
            if "uorod" in cl and "panei" not in cl:
                url_col = c
                break
        if url_col is None:
            log.warning("no Nuoroda column in %s; columns=%s", meta_path, list(df.columns))
            continue
        for _, row in df.iterrows():
            url = (row.get(url_col) or "").strip()
            if not url.startswith("http"):
                continue
            queue.append({
                "id": f"litund:{subset}:{row['Failas']}",
                "subset": subset,
                "failas": row["Failas"],
                "url": url,
                "source_type": src_type,
            })

    if args.limit:
        queue = queue[: args.limit]
    log.info("queued %d LITUND URLs (%d unreliable, %d lrt)",
             len(queue),
             sum(1 for x in queue if x["subset"] == "unreliable"),
             sum(1 for x in queue if x["subset"] == "lrt"))

    # Truncate output JSONL for a fresh run
    out_jsonl.write_text("", encoding="utf-8")

    # Robots cache + per-host rate-limit timestamp
    robots: dict[str, urllib.robotparser.RobotFileParser] = {}
    last_fetch: dict[str, float] = defaultdict(float)

    def get_robots(base: str) -> urllib.robotparser.RobotFileParser:
        if base not in robots:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(urllib.parse.urljoin(base, "/robots.txt"))
            try:
                rp.read()
            except Exception:
                pass
            robots[base] = rp
        return robots[base]

    n_ok = n_failed = n_no_img = n_robot = 0
    for i, item in enumerate(queue, 1):
        url = item["url"]
        parsed = urllib.parse.urlparse(url)
        host = parsed.netloc
        base = f"{parsed.scheme}://{host}"
        rp = get_robots(base)
        try:
            if not rp.can_fetch(ua, url):
                n_robot += 1
                continue
        except Exception:
            pass
        # Per-host rate limit
        elapsed = time.time() - last_fetch[host]
        if elapsed < args.rate_limit_s:
            time.sleep(args.rate_limit_s - elapsed)
        last_fetch[host] = time.time()
        # HTML cache
        h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
        cache_path = cache_root / f"{h}.html"
        try:
            if cache_path.exists():
                html = cache_path.read_text(encoding="utf-8", errors="ignore")
            else:
                resp = _fetch(url, ua, args.timeout_s)
                if resp.status_code != 200:
                    n_failed += 1
                    log.warning("HTTP %d: %s", resp.status_code, url)
                    continue
                html = resp.text
                cache_path.write_text(html, encoding="utf-8")
            img_url = _extract_image_url(html)
            if not img_url:
                n_no_img += 1
                continue
            img_url = urllib.parse.urljoin(url, img_url)
            dst_base = images_root / item["subset"] / item["failas"]
            img_path = _download_image(img_url, dst_base, ua, args.timeout_s)
            if img_path is None:
                n_failed += 1
                continue
            row = dict(item)
            row["image_path"] = img_path
            row["image_url"] = img_url
            append_jsonl(out_jsonl, row)
            n_ok += 1
            if i % 25 == 0:
                log.info("  progress %d/%d  (ok=%d failed=%d no_img=%d robot=%d)",
                         i, len(queue), n_ok, n_failed, n_no_img, n_robot)
        except Exception as e:
            n_failed += 1
            log.warning("failed (%s): %s", url, e)

    log.info("DONE. ok=%d  failed=%d  no_img=%d  robot_blocked=%d  (queue=%d)",
             n_ok, n_failed, n_no_img, n_robot, len(queue))


if __name__ == "__main__":
    main()
