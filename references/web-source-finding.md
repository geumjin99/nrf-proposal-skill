# Finding Web Sources — News, Products, Market Intel (no fabrication)

> Companion to `research-trend-search.md` (papers) and `academic-sources.md` (APIs). A strong
> 연구 동향 / 사업화 / 기대효과 section needs more than papers: market size, product/competitor
> landscape, policy direction, news. This file applies the **same discipline as the local
> `academic-search` skill** to the open web — *every claim carries a resolvable URL; nothing is
> invented.*

## Borrowed philosophy (from academic-search)

> **명확한 목표 → 올바른 출처 → 구조화 데이터 추출 → 완료 즉시 정지.**

1. **Define the goal & success criteria first.** What exactly is needed — market size figure?
   competitor list? policy/regulation? a news fact with a date? Decide what "done" looks like
   before searching.
2. **Two-pass, light-then-deep.** First pass: a lightweight hit list (title, publisher, date, URL,
   one-line gist) — don't deep-read yet. Confirm the 5–10 most relevant/authoritative, *then*
   fetch full content.
3. **Structured extraction, deduped.** Capture a uniform record per source; merge duplicates by
   canonical URL/title. Never paste raw HTML into the proposal.
4. **Use failure signals to change direction** (don't retry the same way):

   | Signal | Meaning | Adjust |
   |---|---|---|
   | WebFetch timeout / JS-only page | not static-fetch friendly | try the publisher's API, a cached/AMP URL, or `r.jina.ai/{url}` |
   | Paywalled / login wall | full text not freely available | cite the public abstract/summary + date; find a primary alt (gov stat, press release) |
   | Zero results | wording or wrong source | change keywords (KR↔EN), switch source class |
   | Same approach fails 3× | wrong path, not "not found yet" | re-scope; switch source/tool |
5. **Stop when the success criteria are met** — don't over-collect.

## Tools available to the skill

- **WebSearch** — discover sources, find the authoritative origin of a claim, get candidate URLs.
- **WebFetch** — pull and extract content from a known URL (articles, reports, product pages).
- **Connected MCP tools** (when present) — e.g. the `academic-search` skill's platform access, or
  Hugging Face paper search for ML topics. Prefer these for academic-flavored queries.
- **`scripts/search_papers.py`** — for the *paper* layer (already verified, returns real DOIs).

## Source-class map (pick by what the claim is)

| Claim type | Authoritative sources (prefer 一手) | Notes |
|---|---|---|
| 시장 규모/성장률 | KOSIS, KIET 산업동향, KISTI KMAPS; Statista/Gartner/IDC (二手, cite summary + year) | gov stats are 一手; consultancy is 二手 — attribute + date |
| 산업/기술 동향 | KISTEP 기술동향 브리프, KIET, 부처 보도자료, 협회 백서 | quantify with KIPRIS patent trends where possible |
| 제품/경쟁사 현황 | company sites, press releases, product docs, 보도자료 | a product *claim* ≠ market truth; label vendor-sourced |
| 정책/규제 방향 | 법령(law.go.kr), 부처 공고/보도자료, 국회/연구기관 보고서 | primary policy text beats news summaries |
| 뉴스/사건 사실 | reputable outlets w/ a dateline; cross-check ≥2 | record the publish date; recency matters |
| 특허/기술 트렌드 | KIPRIS / KIPRIS Plus | filing trend, IPC classes, top applicants = quantifiable 一手 |

(Korean STEM 동향 + the academic layer: ScienceON / KCI / RISS — see `academic-sources.md`.)

## Record schema (one per source)

```
- claim: <the specific statement this supports>
- value/fact: <number / quote / status> (verbatim, with units & year)
- source: <publisher / org>
- url: <resolvable link> ← REQUIRED; no link ⇒ [VERIFY], not a cite
- date: <publish date> (esp. for market/news)
- tier: 一手 (primary: gov stat, law, patent, press release) | 二手 (analysis/news)
```

## Anti-fabrication rules (non-negotiable — same as the paper layer)

- **No URL ⇒ not a citation.** Mark unverifiable statements `[VERIFY: …]` and tell the user.
- **Quote numbers verbatim with unit + year**; never "round up" or interpolate a market figure.
- **Separate 一手 from 二手** in the text; a consultancy estimate is attributed, not stated as fact.
- **A vendor's product claim is a claim, not market truth** — frame it as such.
- If a needed figure can't be sourced freely, **say so** and offer the closest primary alternative
  (a government statistic, a patent trend) rather than inventing a number.

## How it feeds the proposal

- **국내외 연구 동향** → papers (`search_papers.py`) + Korean academic layer.
- **산업/시장 동향 (PART2 §사업화, 기대효과)** → this file's market/industry/policy classes.
- Every line that asserts a fact ends in a resolvable citation; the bibliography/`references.bib`
  collects the academic ones, a "출처" list collects the web ones with dates.
