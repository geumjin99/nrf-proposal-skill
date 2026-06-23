<div align="center">

# 🇰🇷 NRF Proposal Copilot

![NRF Proposal Copilot](assets/hero.png)

### An AI **Skill** that writes *fundable* Korean National Research Foundation (NRF / 한국연구재단) grant proposals — like a seasoned PI, not a chatbot.

[![Skill](https://img.shields.io/badge/Claude-Skill-7C3AED)](#-installation)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Lang](https://img.shields.io/badge/proposal%20output-한국어-blue)](#)
[![Programs](https://img.shields.io/badge/programs-신진·핵심·리더·세종·인문사회-orange)](#-which-programs)

*Plan → research the field live → design the logic → draft in Korean → draw the figures → simulate the review panel → ship.*

[한국어](README.md) · **English**

</div>

---

> **연구계획서, 이제 혼자 쓰지 마세요.**
> This skill doesn't just polish prose. It scouts the literature, builds your 국내외 연구 동향 from
> **real, citable papers**, structures the argument the way reviewers score it, draws your
> 추진체계도 and 간트차트, reads/exports your **HWP(한글)** documents, and then **role-plays an NRF
> review panel** to break your draft in private — so it survives in public.

> ### Responsible use — please read
> NRF and most funders **prohibit submitting AI-generated proposals**, and the text is your own
> scholarly representation. **We do not endorse using AI to write a proposal and submit it.** This
> is a **learning & reference aid** — to study what excellent proposal *structure and writing
> style* look like, scout sources, visualize a plan, and stress-test a draft from a reviewer's
> view. Treat every output as a **draft to rewrite in your own voice and verify** — the science and
> the final words must be yours.

## Why this exists

NRF selection rates run ~10–30%. A panel reviewer reads 5–9 similar proposals and decides each in
**minutes**, often as a *competent outsider, not your sub-field expert*. Winning proposals are
almost never public, so generic "grant writing tips" don't cut it. This skill encodes what
actually moves the score:

- **Score-aligned by design** — 창의성·도전성 is worth **40–50%** of the score, so the skill
  spends your pages and rhetoric there, not where habit says.
- **Evidence, not vibes** — the 연구 동향 section is built from **live search** (OpenAlex,
  Semantic Scholar, Crossref, arXiv, + Korean ScienceON / KCI / RISS), every claim carrying a
  resolvable DOI. **No fabricated citations, ever.**
- **Reviewer-mind baked in** — the 7 reviewer questions, the real point weights per program, and
  the actual rejection list drive both drafting and a 3-reviewer **panel simulation**.
- **Figures that survive 2-up printing** — publication-grade TikZ 추진체계도 / 간트차트 / 개념도,
  in Korean, because reviewers print proposals two-to-a-page and squint.
- **Anti-rework checkpoints** — it confirms your *research gap* and *logic skeleton* with you
  **before** drafting 10 pages on a shaky premise.
- **3-reviewer panel simulation** — modeled on a Nature-style referee skill: a sub-field expert,
  a competent outsider, and a skeptic each score your draft per the official rubric, then a ranked
  fix-list lifts the weak axes. (No invented data, citations, or reviewer identities.)
- 📄 **HWP in, HWP out** — reads your official `.hwp` 양식 / 공고 / sample (handling the nasty
  Korean filename normalization bug) and **writes the proposal as a real HWP file (`.hwpx`)** — no
  PDF. `.hwpx` opens natively in Hancom (save-as `.hwp`), with headings, real tables, and embedded
  figures. *Verified: validate() 0 issues, 3 figures embedded.*
- **Web evidence without fabrication** — market size, competitor/product, policy and news for
  your 기대효과/사업화 sections, every fact pinned to a resolvable URL + date.
- **RFP/공고 → fundable ideas** — extracts hard constraints (품목·TRL·budget·period·score
  weights), hard-filters violators, then scores/ranks ideas on **call-fit · novelty · feasibility ·
  PI-fit**. (LLM ideas skew *novel but less feasible* → it leans on feasibility and call-fit.)
- **Visual-asset planning** — not just text: it tells you *what goes where* (a wildfire news
  photo here, a lab-equipment shot there, a concept diagram here), generating what it can and
  leaving labeled `[비주얼 자리]` placeholders for the rest.
- **TikZ + matplotlib figures** — box-and-arrow (추진체계도/간트차트) in TikZ; data charts
  (perf comparison, TRL roadmap, differentiation radar) in matplotlib, Korean labels and all.
- **Correct fonts, by construction** — `.hwpx` renders in Hancom's own fonts (함초롬바탕 etc.), so
  the font-garble / mixed-font problems of PDF conversion simply don't occur.

## It draws real figures (auto-generated, in Korean)

| 추진체계도 (research framework) | 간트차트 (연차별 일정) |
|:---:|:---:|
| ![pipeline](assets/example_pipeline.png) | ![gantt](assets/example_gantt.png) |
| *Novel module highlighted — it's literally arguing your 창의성 score* | *Milestones + 연차별 bars, the most-expected figure in 추진전략* |

Generated from the bundled `.tex` templates via one command, then handed back as `.tex` + high-res
PNG/PDF to drop straight into your HWP/Word document.

## The 7-phase workflow

```
0 Route & Intake → 분야 (이공/인문사회) + 사업 + 2026 IRIS naming + read your .hwp 양식/공고
1 연구 현황 조사 → live multi-source search → ranked, cited landscape → gap statement
2 논리 골격 설계 → Claims–Aims–Evidence matrix + SMART goals + 차별성 table + page budget
3 본문 집필 → section-by-section Korean draft, each tied to its score dimension
4 그림·도식 생성 → 추진체계도 · 간트차트 · 개념도 (TikZ, compiled + previewed)
5 평가 시뮬레이션 → 3-reviewer panel scores per official rubric → ranked fixes → re-score
6 제출 전 점검·HWP 출력 → page/format gate · IRIS·NRI prerequisites · blind (인문사회) · → .hwpx (HWP)
```

주(Note): mandatory checkpoint with you. Iterating a one-page skeleton is cheap; rewriting ten pages is not.

## Which programs

Routes and adapts to the **2026 IRIS** system and naming (keeps old names as aliases):

| 분야 | 사업 (2026) | old name |
|---|---|---|
| 이공 (과기정통부) | **신진연구**, **핵심연구** (유형C/B/A·도약형), **리더연구**, **세종과학펠로우십**, 기본연구, 한우물파기 | 우수신진, 중견연구 … |
| 인문사회 (교육부) | **신진/중견/우수학자**, 학술연구교수 | — *(blind review enforced)* |

Page limits, eligibility windows, and **exact score weights** per program live in
[`references/`](references/).

## Installation & usage

Clone it once:

```bash
git clone https://github.com/geumjin99/nrf-proposal-skill.git
```

The skill is just a Markdown playbook (`SKILL.md` + `references/`) plus helper `scripts/`, so it
works with **any** agent that reads instructions. Two common setups:

### Claude Code (native Skill)

This is a [Claude Skill](https://docs.claude.com/en/docs/claude-code/skills). Drop the folder where
Claude Code loads skills — it then **auto-loads** when you mention NRF/연구계획서:

```bash
# global (all projects):
cp -r nrf-proposal-skill ~/.claude/skills/nrf-proposal
# or per-project:
cp -r nrf-proposal-skill ./.claude/skills/nrf-proposal
```

### Codex CLI / Cursor / Cline / Gemini CLI (AGENTS.md-style agents)

These have no native skill loader, so point the agent at the playbook yourself. Keep the folder in
or beside your project and add a pointer to your `AGENTS.md` (Codex) — or just tell the agent in
chat to follow it:

```markdown
## NRF 연구계획서
When the user asks to plan/write a Korean NRF (한국연구재단) 연구계획서, follow the playbook in
`./nrf-proposal-skill/SKILL.md` and its `references/`, and use the helper scripts in `scripts/`.
```

### Then just talk to it

> "신진연구 계획서 쓰고 싶어. 주제는 그래프 신경망 기반 단백질 상호작용 예측이야."
> "Follow nrf-proposal-skill/SKILL.md and help me write an NRF 핵심연구 proposal on …"

### Optional dependencies (for the figure & search tooling)

| Feature | Needs | Install (Debian/Ubuntu) |
|---|---|---|
| TikZ figures (Korean) | XeLaTeX + Korean fonts | `sudo apt install texlive-xetex texlive-latex-extra texlive-lang-korean fonts-noto-cjk` |
| PDF→PNG preview | poppler **or** ImageMagick | `sudo apt install poppler-utils` |
| Literature search | Python 3 (stdlib only) | already have it |
| Data charts | matplotlib | `pip install matplotlib` |
| Read HWP(한글) | pyhwp | `pip install pyhwp` |
| Write HWP (.hwpx) | python-hwpx | `pip install python-hwpx` |

The literature scout uses only free, no-key APIs:

```bash
python3 scripts/search_papers.py "graph neural network protein interaction" \
        --email you@example.com --limit 12 --since 2021 --oa
```

## Repository layout

```
nrf-proposal/
├── SKILL.md # the agent's playbook (7 phases)
├── references/ # NRF knowledge base (programs, structure, scoring, search, HWP …)
├── templates/ # Korean proposal skeletons + Claims-Aims matrix + .tex figures
├── scripts/ # search_papers · check_proposal · compile_tikz · make_figure_mpl · hwp_tools(read) · write_hwpx(write .hwpx)
└── assets/ # showcase figures + README image prompts
```

## What it will and won't do

- Structure, scout, draft, visualize, and stress-test a reviewer-aligned proposal.
- Build the 동향 section from verifiable papers and flag everything unverifiable as `[VERIFY]`.
- It will **not** promise "guaranteed selection," invent your results, fabricate citations or
  numbers, or hand you a fake "winning sample." It is honest about the limits of any tool — and
  says so to your face.

## Acknowledgements & sources

Built on official NRF 신청요강 / 연구계획서 양식, 문우경 《성공적인 연구계획서 작성법》 (2022), NRF
웹진, and university 산학협력단 guides. The TikZ figure approach is adapted from the
[`research-figure`](https://github.com/chingswy/Skill-Research-Figure) skill, and the 3-reviewer
panel simulation is modeled on the `nature-reviewer` skill from
[`nature-skills`](https://github.com/Yuan1z0825/nature-skills); thanks to both authors. Always
re-download your target program's 신청요강 before submission — figures and rules change yearly.

## Help build this — a community project

This repo is meant to be **built together, in the open**. NRF rules, forms, and score weights
**change every year** — exactly the kind of thing no single person keeps current. Contributions are
very welcome, especially:

- **Per-program 평가표 / 배점 updates** and 인문사회 evaluation tables (an open TODO).
- **HWP(.hwpx) formatting & layout fidelity** (an active work-in-progress — alignment, tables, form match).
- Worked examples, reference corrections, new search sources, translations.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and open an issue or PR — small fixes welcome. 화이팅!

## License

[MIT](LICENSE). Contributions welcome — especially per-program 평가표 updates and worked examples.

<div align="center">
<sub>Made for researchers who'd rather do research than fight a proposal template. · 화이팅! </sub>
</div>
