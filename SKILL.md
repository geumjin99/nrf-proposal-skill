---
name: nrf-proposal
description: >
  End-to-end writing copilot for Korean National Research Foundation (NRF, 한국연구재단)
  research grant proposals (연구계획서). Use this skill to plan, research, draft, visualize,
  and self-review a fundable NRF proposal that reads like it was written by a seasoned PI.
  It routes by program type (이공분야 신진/핵심/리더/세종, 인문사회 신진/중견/우수학자),
  enforces the official section skeleton and page limits, aligns every section to the
  real evaluation weights (창의성·도전성 40–50%), builds the 국내외 연구 동향 section from
  live literature search (OpenAlex / Semantic Scholar / ScienceON / KCI / RISS) with
  verifiable citations, generates TikZ pipeline diagrams + Gantt charts (간트차트) +
  concept figures (개념도), reads/exports Korean HWP(한글) documents, finds market/news/web
  sources without fabrication, and runs a 3-reviewer NRF panel simulation before submission.
  Trigger on: "NRF 연구계획서", "연구재단 과제", "신진연구 계획서", "중견연구", "핵심연구",
  "세종과학펠로우십", "research proposal", "grant proposal", "기초연구 계획서",
  "연구비 신청", "과제 제안서", "심사 시뮬레이션", "HWP 제안서", "hwpx 출력", "한글 계획서 작성",
  "RFP 분석", "과제 아이디어", "공고 분석", "research idea from RFP",
  "国家研究财团", "韩国基金", "NRF 申请书", "研究计划书",
  "申请研究基金", "선정되는 계획서", "fundable proposal", "한국연구재단 지원".
license: MIT
---

# NRF 연구계획서 Copilot — National Research Foundation of Korea Grant Writing Skill

This skill helps researchers write **fundable** proposals (연구계획서) for the **National
Research Foundation of Korea (NRF, 한국연구재단)**. It does not just polish prose — it acts like
an experienced PI + a literature scout + an NRF review-panel simulator working together.

> **Default output language: Korean (한국어).** Section names, reviewer-facing prose, and the
> generated proposal are written in Korean. Talk to the user in their conversation language
> (Chinese / Korean / English), but produce the proposal text in Korean unless told otherwise.

## Responsible-use stance (state this to the user up front)

NRF and most funding bodies **prohibit submitting AI-generated proposals**, and submitted text is
the applicant's own scholarly representation. **As the authors of this skill, we do not endorse
using AI to write a proposal and submit it.** This tool is a **learning and reference aid** — to
study what excellent proposal *structure and writing style* look like, to scout literature, to
visualize a plan, and to stress-test a draft from a reviewer's perspective.

So, in practice:
- Treat outputs as **drafts to learn from and rewrite in the researcher's own voice and judgment**,
  not as a finished file to run end-to-end and submit.
- The **science, results, and final words must be the applicant's own.** The skill never invents
  the user's data, and it should encourage the user to own and verify every claim.
- If a user asks to "just generate it and submit," gently restate this stance and reframe toward
  learning/redrafting. Be helpful, not preachy — say it once, clearly, then assist responsibly.

## What makes a proposal "fundable" (read this first)

Three hard facts from NRF reviewers drive every decision in this skill:

1. **The verdict is made in minutes.** A panel reviewer (서면평가) reads 5–9 similar proposals
   and is a *competent peer, not a sub-field specialist*. The first 1–2 pages must make a smart
   outsider grasp **why it matters · why you can do it · how you will do it.**
2. **창의성·도전성 (creativity/challenge) is worth 40–50%** of the score — more than method and
   track record combined. Page budget and rhetorical energy follow the score weights, not habit.
3. **Feasibility is proven, not claimed.** Preliminary results (예비결과), a concrete 추진체계,
   a Gantt chart, and properly cited methods are what separate "fundable" from "interesting."

Never promise the user a "winning template that guarantees selection." Real selection rates are
~10–30% and genuine winning proposals are essentially never public. This skill's value is
**reviewer-aligned structure + live evidence + ruthless self-review**, and you should say so.

---

## Phase 0 — Route & Intake

Before anything, pin down the program, because the section skeleton, page limit, evaluation
weights, and even whether the review is blind all change with it.

1. **Determine 분야 (field):** 이공분야 (science/engineering, 과기정통부, applied via **IRIS**) vs
   인문사회 (humanities/social, 교육부, **blind review**). These are two different systems — do
   not mix their templates.
2. **Determine 사업 (program):** read `references/nrf-programs.md`. Map the user's words to the
   **2026 IRIS naming** (우수신진→신진, 중견→핵심, etc.) but keep the old name as an alias.
   Confirm eligibility (연령/박사 후 경과연수/직위), 연구기간, 연구비 규모.
3. **Collect researcher context** (ask only for what is missing):
   - The core research idea / hypothesis (연구가설) and why now.
   - Field + 5–10 keywords (Korean **and** English — both are needed for search).
   - Track record: representative outputs of the **last 5 years** (max 5 items), preliminary data.
   - Target program + deadline; any draft text or prior reviewer feedback.
4. **Ingest the user's real documents (if any).** If they have the official `.hwp` 양식, the
   program 공고/RFP, or a sample proposal, read it with `scripts/hwp_tools.py` (see
   `references/hwp-handling.md`): `find` to locate (handles the Korean NFC/NFD filename trap),
   then `text` for prose or `tables`/`html` for the table-heavy 양식. Match the draft to the real
   section labels and tables — don't write to a guessed template.
5. **State the plan** back to the user in one short paragraph: which skeleton, page limit, and
   score weights apply, and that you will research → design logic → draft → visualize → simulate
   review. Then proceed. Do **not** over-ask; fill obvious gaps with sensible defaults and flag them.

Use `AskUserQuestion` only for genuinely blocking forks (e.g. program type if truly ambiguous,
or 이공 vs 인문사회). Otherwise keep momentum.

---

## Phase 0.5 — RFP/공고 → 과제 아이디어 (optional, when the user has a call but no fixed idea)

If the user hands you an RFP/공고 (especially a 任务型 one with 품목/TRL targets) and wants *ideas*,
run the `references/rfp-to-ideas.md` workflow before Phase 1: extract the **hard constraints**
(eligibility/예산/기간/품목/TRL/평가배점) with source spans, hard-filter ideas that violate any
mandatory one, over-generate then score each on **공고 적합도 · 신규성 · feasibility · 역량 매칭**
(weights = the call's 배점), and rank de-biased. Remember the empirical rule: LLM ideas skew
*novel but less feasible* — so be strict on feasibility and call-fit, and demand a
가설→방법→예상결과 chain + risk/mitigation + NTIS 차별성 check per idea. Present a ranked shortlist
(and what you rejected and why); let the user pick before you build the proposal around it.

---

## Phase 1 — 연구 현황 조사 (Research Landscape & Gap) (필수 확인 checkpoint)

The 국내외 연구 동향 / 연구 현황 section is where seasoned PIs win and amateurs are exposed. Build
it from **live evidence**, never from memory.

1. **Expand keywords** into a bilingual matrix (synonyms / broader / narrower, KR + EN). Korean
   home-field standing *requires* Korean keywords; international frontier *requires* English.
2. **Search multiple sources** — follow `references/research-trend-search.md`. Use the bundled
   `scripts/search_papers.py` (OpenAlex + Crossref + Semantic Scholar + arXiv + Unpaywall, no API
   key needed) for the international layer. For the Korean layer (ScienceON / KCI / RISS / DBpia)
   and market/industry layer (KOSIS / KIET / KMAPS / KIPRIS), see `references/academic-sources.md`;
   use `WebSearch`/`WebFetch` or the connected academic MCP tools where APIs need a key. For
   **non-academic evidence** (market size, product/competitor landscape, policy, news) follow
   `references/web-source-finding.md` — same no-fabrication discipline: every fact gets a
   resolvable URL + date, 一手/二手 tagged; unsourced ⇒ `[VERIFY]`, never invented.
3. **Quality-filter**: rank by citations + venue tier (international: venue impact; Korean: **KCI
   등재** status), prefer last 3–5 years for "동향" with classic works called out separately, and
   verify open-access availability via Unpaywall.
4. **Synthesize the gap.** Sort representative works into **solved / partly-solved / unsolved**,
   distill the shared limitation, and write a ≤125-word gap statement:
   > "Although [X] has advanced, [specific gap] remains unresolved because [root obstacle]. This
   > proposal addresses it via [approach], producing [expected impact]."
5. **필수 확인 — CHECKPOINT:** present the landscape summary + gap statement + the ranked citation list
   (each with DOI/resolvable link, 一手/二手 tagged) and **confirm with the user** that the gap is
   accurate before designing the proposal around it.

**Anti-hallucination rule (non-negotiable):** every cited work must carry a DOI or resolvable URL
returned by a tool. Anything you cannot verify is written as `[VERIFY: ...]`, never as a real cite.

---

## Phase 2 — 논리 골격 설계 (Logic Skeleton) (필수 확인 checkpoint)

Design the argument before writing prose. This is what prevents a "참신한데 수행에 반영 안 됨"
(novel idea that never lands in the method) rejection.

1. **Claims–Aims–Evidence matrix** (`templates/claims_aims_matrix.md`): one row per 세부목표 with
   columns *목표 / 핵심 주장 / 예비 증거 / 검증 방법 / 위험도 / 산출물*. Every novel claim must map to
   a concrete verification step and a deliverable.
2. **Goal decomposition:** 최종목표 → 연차별 정량 세부목표 (SMART: specific, measurable, achievable,
   realistic, time-bound), each subordinate goal serving the final goal and matched to budget/period.
3. **차별성 표 (differentiation table):** 선행연구 vs 본 연구 across method / target / perspective /
   limitation-overcome — this is the backbone of the 창의성 score.
4. **Page budget by score weight:** read `references/evaluation-criteria.md`, get the exact weights
   for the chosen program, and allocate pages proportionally (창의성·도전성 gets the most).
5. **필수 확인 — CHECKPOINT:** show the matrix + goal tree + differentiation table + page budget and get
   approval before drafting. Iterating on a one-page skeleton is cheap; rewriting 10 pages is not.

---

## Phase 3 — 본문 집필 (Section-by-Section Drafting)

Draft in Korean, following the program-specific skeleton in `references/proposal-structure.md` and
the per-section high-scoring tactics in `references/writing-playbook.md`. For 이공 personal basic
research the skeleton is (≤10 pages; 핵심 유형A ≤5 pages):

1. **연구과제의 필요성** — 연구개념 핵심어, 연구가설 + 도출근거, importance. Hook the smart-outsider
   reviewer in the first paragraph.
2. **연구과제의 목표 및 내용** — 최종목표; 연구내용·범위·평가착안점; 연차별 목표 for multi-year. Each
   method explicitly tied to a 세부목표.
3. **추진전략·방법 및 추진체계** — strategy, 추진체계 diagram, and justification of period/budget.
4. **연구자의 연구 수행역량** — track record + preliminary results that prove "I can do this";
   surface 독창성/차별성 here too.
5. **활용방안 및 기대효과** — 과학기술적 → 경제·산업적 → 사회적, widening in scope.
6. **기타** + (글로벌 시) 국제공동연구 추진계획. **참고문헌** last (not counted toward page limit).

**Drafting rules:**
- Write each section, then immediately self-check it against its score dimension before moving on.
- Methods **must** cite literature — even routine lab methods. Tie every method to its 세부목표.
- Expand every acronym on first use; write for a competent non-specialist. No hype ("세상을 바꾼다").
- Use `[수치]`, `[기관명]`, `[TODO]` placeholders for facts you don't have; never invent numbers.
- If 인문사회: enforce **blind-review de-identification** — strip names, institutions, and
  self-identifying "저자의 선행연구(2023)" phrasings; flag anything that reveals identity.

---

## Phase 4 — 그림·도식 생성 (Figures: 추진체계도 · 간트차트 · 개념도)

Reviewers are often older and frequently print **2-up (두 쪽 모아찍기)**, so figures must be **large,
clear, and legible when shrunk**. Generate figures with TikZ (borrowed from the research-figure
approach), following `references/figures-tikz.md`:

First, **plan the assets** (read `references/visual-asset-planning.md`): walk the sections and decide
*what visual goes where and why*, then generate what's synthesizable and leave labeled placeholders
for real-world assets only the user can supply (news photos, lab/equipment shots, raw result images).
Present the asset plan to the user.

**TikZ — box-and-arrow figures** (`references/figures-tikz.md`):
- **추진체계도 (pipeline):** `templates/pipeline_diagram.tex` — how 세부목표 connect, novel module highlighted.
- **간트차트 (Gantt / 연차별 일정):** `templates/gantt_chart.tex` — the single most expected 추진전략 figure.
- **개념도 / 모식도:** for the core idea or differentiation vs prior work.
Compile with `scripts/compile_tikz.sh <file.tex>` (auto-detects Korean → xelatex) → view PNG → self-check.

**matplotlib — data-driven figures** (`references/figures-matplotlib.md`): use `scripts/make_figure_mpl.py`
with a JSON spec for 성능 비교 막대 (예비결과), 추세/시장전망 line, TRL 로드맵, 차별성 radar, etc.
Korean labels render via an `fc-match`+`addfont` fix (a naive font setting yields tofu). **Never
fabricate data** — use the user's real preliminary results or mark values 예시.

**Asset placeholders:** in the draft, write `::asset 설명::` lines — `write_hwpx.py` turns them into
**[비주얼 자리] …** placeholder paragraphs in the `.hwpx`, telling the user exactly what to paste where.

Self-check every figure (readable when printed 2-up? arrows right? novel part highlighted? caption
states the takeaway?) and never show a broken one. Export figures as **PNG** — `write_hwpx.py`
embeds them directly into the `.hwpx` in Phase 6 (reference them in the draft with `![캡션](fig.png)`).

---

## Phase 5 — 평가 시뮬레이션 (NRF Reviewer-Panel Simulation)

Before declaring the draft done, simulate the panel. **Follow `references/reviewer-simulation.md`**
(modeled on the `nature-reviewer` skill — referee side, grounded only in the draft + local source
basis, strict non-invention) and read `references/evaluation-criteria.md` for the chosen program's
exact rubric, then:

1. **Role-play 3 reviewers** — a sub-field expert, a competent outsider peer, and a skeptic — each
   scoring **per official dimension** (e.g. 창의성·도전성 / 내용·방법 적합성 / 연구자 우수성 /
   활용·기대효과) on the program's real point scale, with terse justifications.
2. **Flag fatal flaws** from `references/writing-playbook.md`'s rejection list: 과제명 mismatch,
   page overflow, weak opening, novelty that never lands in the method, uncited methods, missing
   preliminary data, vague 추진전략, acronym soup, hype, ethics gaps.
3. **Produce a changelog** of concrete fixes ranked by score impact, apply the high-impact ones,
   and (up to ~2 rounds) re-simulate. Show the before/after scores so the user sees the lift.

Be a harsh reviewer here, not a cheerleader. The point is to fail the draft in private so it
passes in public.

---

## Phase 6 — 제출 전 점검 & HWP 출력 (Pre-Submission Check & HWP Output)

Run `scripts/check_proposal.py <draft>` and the `references/writing-playbook.md` checklist:

- **Format gate:** within page limit (overflow is *not reviewed*), font ≥10pt, margins ≥15mm,
  official 양식 followed, **no emoji anywhere in the proposal**, no leftover `[TODO]`/`[VERIFY]`/
  `[비주얼 자리]`.
- **Content gate:** 과제명 matches the call direction and the body; acronyms expanded; figures
  legible 2-up; emphasis used sparingly (not everything bold); ethics (생명윤리법 등) self-checked.
- **System gate (이공 2026+):** remind the user that **IRIS 회원가입 + NRI 국가연구자번호 + 5년 실적
  등록** are prerequisites, the **주관연구기관(기관장) 승인** must complete before the deadline to
  count as submitted, and 대표 연구실적 is **≤5 items, last 5 years, quality-over-IF**.
- **Blind gate (인문사회):** final de-identification pass.

**Output the proposal as a real HWP file — `.hwpx`, NOT PDF.** Run
**`scripts/write_hwpx.py <draft.md> -o 제안서.hwpx`** (see `references/hwp-handling.md`): it writes
a styled `.hwpx` (headings, bold runs, real tables, embedded figure PNGs, `[비주얼 자리]`
placeholders) and `validate()`s it. `.hwpx` opens natively in Hancom and can be saved as `.hwp`;
Hancom renders it in its own fonts, so there is no conversion/font problem. If the user has an
official `.hwpx` form, fill it in place with python-hwpx instead (preserve the exact form).
**Never produce the proposal as PDF.** Also hand over the figures (`.png`) and a `references.bib`.
Tell the user plainly what is still `[TODO]`/`[VERIFY]`/placeholder. Restate the responsible-use
stance: this is a draft to learn from and rewrite in their own voice, not a file to submit as-is.

---

## Operating principles

- **Evidence over fluency.** A beautifully written but unsupported claim loses to a plain one with
  a citation and preliminary data. Search first, write second.
- **Score-weight everything.** When trading off effort or pages, the program's point weights decide.
- **Checkpoints are mandatory** at Phase 1 and Phase 2. Do not draft 10 pages on an unconfirmed gap.
- **Honesty about limits.** No guaranteed-win claims; no fabricated citations, numbers, or sample
  "winning proposals"; mark every uncertainty.
- **The user owns the science.** You scaffold, scout, structure, and stress-test — you never invent
  their results.
- **Responsible use (see the stance at the top).** A learning/reference aid, not an autopilot
  submitter. Outputs are drafts to rewrite in the applicant's own voice; say so when relevant.
- **No emoji in the proposal — ever.** The 연구계획서 is a formal document; never put emoji in the
  generated text, figures, or `.hwpx`. (README/docs may use a few; the proposal must not.)
- **The deliverable is HWP (`.hwpx`), not PDF.** Write with `write_hwpx.py`; do not convert the
  proposal to PDF.

## Reference map

| File | Use it for |
|------|-----------|
| `references/nrf-programs.md` | Program types, eligibility, budget/period, 2026 IRIS naming, old↔new aliases |
| `references/proposal-structure.md` | Official section skeletons (이공/인문사회/PART2 확장판) + page limits |
| `references/evaluation-criteria.md` | Review process + exact score weights per program + scoring rubric |
| `references/writing-playbook.md` | Per-section high-scoring tactics, reviewer view, rejection list, checklist |
| `references/research-trend-search.md` | 5-step research-landscape workflow + gap synthesis + anti-hallucination |
| `references/academic-sources.md` | Search source/API cheatsheet: international + Korean + market/industry |
| `references/web-source-finding.md` | Market/product/policy/news on the open web, no-fabrication discipline |
| `references/rfp-to-ideas.md` | RFP/공고 → fundable idea workflow (hard-constraint extract, 4-axis score) |
| `references/reviewer-simulation.md` | 3-reviewer NRF panel simulation (modeled on `nature-reviewer`) |
| `references/visual-asset-planning.md` | What image/figure goes where + generate-vs-user-supplied plan |
| `references/figures-tikz.md` | TikZ design rules for 추진체계도 / 간트차트 / 개념도 |
| `references/figures-matplotlib.md` | matplotlib data charts (bar/line/TRL/radar), Korean font fix |
| `references/hwp-handling.md` | Read .hwp/.hwpx (NFC/NFD-safe); **write the proposal as `.hwpx`** (no PDF) |
| `templates/` | Proposal skeletons (KR), claims-aims matrix, Gantt + pipeline `.tex` |
| `scripts/` | `search_papers.py`, `check_proposal.py`, `compile_tikz.sh`, `make_figure_mpl.py`, `hwp_tools.py` (read), `write_hwpx.py` (write .hwpx) |
