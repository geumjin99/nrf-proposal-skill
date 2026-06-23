# RFP / 공고 → Fundable Research Ideas (과제 아이디어 도출)

> Read an RFP/공고 and propose **concrete, doable, and competitive** research ideas — not vague
> wishes. Grounded in the patterns of open research-ideation systems (Stanford AI-Researcher,
> AI-Scientist, Google co-scientist, ResearchAgent, SciMON) and NRF's real scoring. **Key empirical
> finding (Si et al., ICLR'25; IdeaBench; SciMON, triangulated): LLM ideas tend to be *novel but
> less feasible* — so this workflow spends its effort on feasibility and call-fit, exactly the axes
> NRF weights most and LLMs do worst.**

## A. Two things to internalize first

1. **Novelty is cheap; feasibility + call-fit are the moat.** Over-generating clever ideas is easy.
   What wins NRF is an idea that is *doable in the period/budget by this PI* and *matches the call's
   evaluation axes*. Score and rank for those.
2. **Know the call type (route first):**
   - **자유공모 (NRF 개인기초연구):** no fixed topic/품목/TRL — ideas are judged on
     창의성·도전성 first. Most individual researchers are here.
   - **任务型 (산업부/KEIT/KIAT, 품목·지정주제·TRL 목표):** the RFP fixes the 품목, target TRL
     (often 5–8), and deliverables — ideas must hit those hard constraints exactly.
   The drone disaster-safety RFP in this repo's test data is the 任务型 kind (has 품목/TRL).

## B. Workflow

### Step 0 — Route
Decide 자유공모 vs 任务型 (above). This decides whether you must parse 품목/TRL targets.

### Step 1 — Extract the hard constraints (type them, with source spans)
Parse the RFP/공고 (use `scripts/hwp_tools.py text|tables` for `.hwp`) into a structured record —
and **quote the source line for each field** (anti-fabrication):
```
지원대상/eligibility · 예산 상한(직접비; 간접비 별도) · 연구기간 · 품목/지정주제 ·
TRL 목표(시작→종료) · 평가지표와 배점 · 우대사항 · 차별성/중복 요건 · 필수 산출물
```
Tag each as **mandatory (shall/must/이어야 함)** vs **preferred (우대/should)**. An idea that
fails a *mandatory* constraint is **hard-filtered out** — no matter how exciting.

### Step 2 — Ground the gap
Search the field (`research-trend-search.md` + `search_papers.py`) **and check NTIS / prior
funded projects** for overlap. Sort the landscape into solved / partly-solved / **unsolved**, and
surface the gaps the RFP's intent points at. (NRF enforces a 차별성·중복성 검토 against NTIS — so
do it here, proactively.)

### Step 3 — Over-generate, then dedupe
Generate **many** seed ideas that already satisfy the Step-1 hard constraints, then dedupe by
semantic similarity (drop near-duplicates). Breadth first; pruning next.

### Step 4 — Score each idea on 4 axes (weight = the call's 배점)
| Axis | How to judge | Note |
|---|---|---|
| **공고 적합도 (call-fit)** | matches 품목/TRL/기간/예산/평가지표? | the "fundable" axis LLMs ignore — **make it a gate or top weight** |
| **창의성·신규성** | literature-grounded: retrieve related work, then **facet-rerank** (purpose/mechanism/evaluation), not cosine-only | cosine-only novelty collapses (89.7%→13.8% recall); always facet-rerank |
| **feasibility** | anchored 1–10: *doable in the period, within budget, by this team, to the target TRL?* | LLMs over-rate this — be strict, consider a human-rerank pass |
| **연구자 역량 매칭** | does the PI's track record cover the skills this idea needs? | maps to NRF 연구자 우수성 |

Set the weights to the **target call's actual 배점** (e.g. 창의성 50 / 적합성 30 / 연구자 10 /
기대효과 10 — see `evaluation-criteria.md`).

### Step 5 — Rank, de-biased
Rank by pairwise comparison (Swiss-tournament style). Watch for LLM-judge pitfalls: position/length
bias and **non-transitivity (A>B>C>A)** — if a cycle appears, fall back to the anchored pointwise
scores. Use an odd-numbered multi-perspective panel to reduce single-judge bias.

### Step 6 — Hard guardrails against "infeasible / generic" ideas
Every surviving idea must come with:
- a **가설 → 방법 → 예상결과 chain**, explicit **baselines/ablation**, and a **risk + mitigation**;
  if it can't be filled, the idea is not feasible — drop it.
- a **차별성 self-check** vs NTIS/prior work (overlap ⇒ downgrade).
- **grounding**: no idea without literature/data support survives.
- a one-line **"왜 이 팀이 이걸 할 수 있나"** tied to the PI's record.

## C. Output format (present to the user)

```
[공고 요약]
- 유형: 자유공모 | 任务型(품목/TRL)
- 하드 제약(출처 span): eligibility / 예산상한 / 기간 / 품목·TRL / 평가배점 / 차별성요건

[아이디어 N개 — 적합도순]
#k. <한 줄 제목>
   · 핵심 가설: · 접근/방법: · 예상 산출물·TRL 도달:
   · 공고 적합도: [상/중/하] (어느 평가지표·품목에 부합)
   · 신규성: [상/중/하] (선행연구 대비 차별점 + 근거 DOI[VERIFY])
   · feasibility: [상/중/하] (기간·예산·역량·TRL 근거)
   · 역량 매칭: [상/중/하] (PI 어떤 실적이 받쳐주나)
   · 리스크 → 완화: · 차별성(NTIS 대비):
[탈락시킨 아이디어와 사유] ← 하드 제약 위반/중복/근거부족은 숨기지 말고 기록
```

## D. Honesty & compliance

- Mark every cited support `[VERIFY]` until it has a resolvable DOI/URL — never invent a reference
  to make an idea look grounded.
- Funders restrict AI-generated *applications*; this is **ideation + self-check support**, with a
  human in the loop (see the responsible-use stance in `SKILL.md`). Say so.
- NRF scoring tables carry "세부평가계획에 따라 변경 가능" — let the user override default weights
  with the actual call's 배점.

## E. Reference projects (for maintainers)

Open-source, most reusable first: **NoviScl/AI-Researcher** (retrieve→over-generate→dedupe→rank→
novelty/feasibility filter), **SakanaAI/AI-Scientist v1/v2** (novelty via Semantic Scholar + auto
review), **llnl/open-ai-co-scientist** & **The-Swarm-Corporation/AI-CoScientist** (Reflection scores
novelty+feasibility, Elo ranking), **lamm-mit/SciAgentsDiscovery** (knowledge-graph concept paths),
**ChicagoHAI/hypothesis-generation**, **run-llama/auto_rfp** (the only OSS that structurally parses
RFPs — but extracts "questions," not eligibility/budget/TRL, which is our differentiation).
Papers: Si et al. *Can LLMs Generate Novel Research Ideas?* (arXiv:2409.04109), ResearchAgent
(2404.07738), SciMON (2305.14259), Google AI co-scientist (2502.18864), Chain-of-Ideas
(2410.13185), IdeaBench (2411.02429), Idea Novelty Checker (2506.22026). Survey hub:
github.com/du-nlp-lab/LLM4SR.
