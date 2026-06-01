# Annotation rubric — 3-class Lithuanian propaganda labelling

**Class space:** `non` · `open` · `hidden`

This rubric governs both the LLM agent (Claude Code in the loop) and human annotators
on the gold subset. Written before any labelling. Cohen's κ ≥ 0.6 between LLM agent
and human gold is required (per CLAUDE.md) for the agent labels to be usable.

---

## 1. Definitions

### non — not propaganda
Reporting that conveys verifiable events, attributes claims to identifiable sources,
balances or transparently signals opinion, and does **not** systematically push a
political agenda through emotional or rhetorical manipulation.

> Examples: a neutral LRT news bulletin on local infrastructure; a factual EU policy
> summary; a sports report; an opinion column clearly marked as opinion that does not
> attack out-groups.

### open (overt) propaganda
The persuasive intent is **visible**. The article uses System-1-targeting techniques
that any attentive reader can spot: name-calling, loaded language, slogans,
flag-waving, explicit fear/anger appeals, repetition, exaggeration, black-and-white
framing.

> Examples: an article that calls a foreign leader by an insulting nickname throughout;
> headlines with shouting capitals and emotive interjections; ritual repetition of a
> nationalist slogan; explicit threats ("the West will collapse"). Style itself flags
> the manipulation.

### hidden (covert) propaganda
The persuasive intent is **disguised** as ordinary reporting. The article reads
plausibly neutral on a quick scan but uses framing, selective quotation, "just
asking questions" doubt, false-balance, appeal-to-authority, whataboutism, or
implicit narrative arcs to advance a specific agenda. Hidden propaganda **bypasses
System-2 scrutiny** — the danger is precisely that it does not look propagandistic.

> Examples: an article that "just reports" Kremlin talking points alongside isolated
> Western quotes for cosmetic balance; an article that consistently chooses the
> sympathetic frame for one side and the unsympathetic frame for the other without
> using any obviously loaded words; selectively chosen experts whose institutional
> backing is omitted.

---

## 2. Decision procedure

1. **Read the full article**, not just the headline.
2. Ask: **does this systematically push a political agenda?**
   - No → `non`.
   - Yes → continue.
3. Ask: **is the manipulation visible at the surface level** (loaded vocabulary,
   slogans, shouting headlines, name-calling, explicit emotional appeals)?
   - Yes → `open`.
   - No, the article reads neutrally but the **framing / selection / implicit
     narrative** does the work → `hidden`.
4. If you cannot decide, mark `confidence < 0.6` and route to the abstain bucket.
   Do **not** force a label.

---

## 3. Worked examples (Lithuanian)

### Example 1 — `non`
> *"Vilniaus savivaldybė pirmadienį paskelbė, kad nuo birželio pradžios viešasis
> transportas dirbs pagal vasaros tvarkaraštį. Naujasis grafikas paskelbtas
> savivaldybės interneto svetainėje; pakeitimai liečia 12 maršrutų."*

Pure factual reporting, attribution to a clear source, no emotive framing.

### Example 2 — `open`
> *"Nuolat meluojantis Vakarų marionetės režimas vėl bandė apgauti tautą — bet
> tauta žino tiesą! Šlovė kovojantiems už tikrąją laisvę!"*

Loaded labels ("marionetės režimas"), shouting slogans, explicit us/them, exclamation
marks. Style flags the propaganda.

### Example 3 — `open`
> Headline: *"ŠOKAS: NATO planuoja kruvinas provokacijas Baltijos pasienyje"*
> Body repeats *"agresyvus NATO blokas"* six times across eight paragraphs.

Sensational headline, loaded epithet repeated as a stylistic device, no balancing
sourcing.

### Example 4 — `hidden`
> *"Tarptautinės politikos ekspertas dr. X aiškina, kad sankcijos labiau kenkia
> patiems vakariečiams. 'Statistika kalba pati už save', — sako jis. Tuo tarpu
> oficialūs Kijevo pareiškimai prieštarauja tikrovei lauke."*

Reads sober and "balanced". But: only one expert quoted; his affiliation omitted;
counter-evidence dismissed as "official statements contradicting reality"; the
sceptic frame is presented uncontested. The manipulation is in the selection and
framing, not the vocabulary.

### Example 5 — `hidden`
> *"Vis daugiau europiečių abejoja paramos Ukrainai prasme. Klausimas paprastas:
> kiek dar metų mes mokėsime už karą, kuris nesibaigia?"*

"Just asking questions" framing (doubt). No insults. The article never says
"stop supporting Ukraine" but every framing nudges in that direction.

### Example 6 — `non` (opinion, but transparent)
> *"Komentaras. Manau, kad ši reforma yra klaida. Štai trys priežastys..."*

Explicitly marked as opinion (*Komentaras*), uses *Manau* ("I think"), gives reasons.
Transparent advocacy is not propaganda.

---

## 4. Edge cases

- **Quoted propaganda inside a debunking article.** The host article is critical of
  the propaganda → `non`. (HALT-PROP labels this `propagandaCitation`; we exclude
  from the 3-class gold set.)
- **Satire / opinion columns.** Classify by the actual content, not the genre label.
- **Translated foreign content** still counts; do not give it a pass.
- **Mixed signals** (some overt + some subtle). If any overt device is present,
  prefer `open`. Hidden propaganda is reserved for articles where the manipulation
  is *only* implicit.

---

## 5. Output format

For each article, the annotator (LLM agent or human) emits:

```json
{
  "id": "<article id>",
  "label": "non | open | hidden",
  "confidence": 0.0,
  "rationale": "<2–3 sentences pointing to specific evidence>",
  "features": {
     "loaded_lexicon": true,
     "us_vs_them": false,
     "selective_framing": true,
     "...": "..."
  }
}
```

If `confidence < 0.6`, route to the human review queue instead of forcing a label.
