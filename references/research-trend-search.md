# Research-Landscape Workflow (국내외 연구 동향) + Gap Synthesis

> The 동향/현황 section is built from **live evidence**, never memory. This is the 5-step workflow
> the skill runs in Phase 1. Source/API details are in `academic-sources.md`; the runnable helper
> is `scripts/search_papers.py`.

---

## Step 1 — Keyword expansion (bilingual)

From the research topic, extract core concepts and build a matrix:
- **synonyms / broader / narrower** terms,
- **English** (for the international frontier) **and Korean** (for the home-field standing).

Use OpenAlex `concepts`/`topics` and Semantic Scholar related terms to discover variants. Korean
home-field search **requires** Korean keywords; international search **requires** English ones.

## Step 2 — Multi-source parallel search

- **International:** `scripts/search_papers.py "<query>"` → OpenAlex (primary) + Crossref +
  Semantic Scholar (high-cited / recommendations) + arXiv (frontier preprints).
- **Korean:** ScienceON (papers + patents + national R&D reports) + KCI (journal tier / stats) +
  RISS (theses) + DBpia (full-text). Most need a key — use `WebSearch`/`WebFetch` or connected
  academic MCP tools when the script can't reach them.
- **Market / industry** (for 사업화 / 기대효과): KOSIS + KIET + KMAPS + KIPRIS (patent trends).

For every result record: **title, authors, year, DOI, citations, venue, source API, 一手/二手 tag.**

## Step 3 — Quality filter

- **Citations** (OpenAlex/Semantic Scholar) → pick representative works.
- **Venue tier:** international = venue impact; Korean = **KCI 등재/등재후보** status.
- **Recency:** "동향" favors last **3–5 years**; list foundational classics separately.
- **OA check:** Unpaywall → get a verifiable full-text link.
- **Anti-hallucination:** every citation needs a DOI/resolvable link; unresolvable → `[VERIFY]`.

## Step 4 — Gap synthesis

Sort representative works into **solved / partly-solved / unsolved**, distill the shared
limitation, and write the ≤125-word gap statement:

> "Although [X] has advanced, [specific gap] remains unresolved because [root obstacle]. This
> proposal addresses it via [approach], producing [expected impact]."

** Confirm the gap with the user before building the proposal around it.**

## Step 5 — Write the 국내외 연구 동향 section

Structure:
1. **국외 동향** — international frontier (high-cited / top venues).
2. **국내 동향** — domestic state & shortfalls (KCI / ScienceON / RISS).
3. **산업/기술 동향** — data from KIET / KMAPS / KIPRIS (patent trends are quantifiable 一手 evidence).
4. **연구공백 & 본 연구의 차별화 위치** — where you fit.

Each claim carries a verifiable citation; 一手 data and 二手 syntheses are tagged separately; output
a `references.bib`. (一手 = primary bibliographic/full-text records; 二手 = national R&D reports,
KISTEP tech briefs, market analyses — use 一手 for facts, 二手 for framing, always attributed.)

---

## Worked mini-example (shape only)

```
topic: "그래프 신경망 기반 단백질 상호작용 예측"
KR kw: 그래프 신경망, 단백질-단백질 상호작용, 딥러닝 신약개발
EN kw: graph neural network, protein-protein interaction, GNN drug discovery

→ search_papers.py "graph neural network protein-protein interaction"
→ OpenAlex top-cited (2021-2025) + arXiv 2024-2025 preprints + KCI 국내 동향
→ filter: keep >50 cites OR top-venue OR last-2yr-frontier; Unpaywall OA links
→ gap: "GNN PPI 예측은 정확도는 올랐으나 [동적 상호작용/희소 종 데이터]는 미해결 —
        본 연구는 [시계열 그래프 + 메타러닝]으로 해결, [희소 종 신약 타깃 발굴]에 기여."
→ confirm with user → write 동향 section with cited claims + references.bib
```
