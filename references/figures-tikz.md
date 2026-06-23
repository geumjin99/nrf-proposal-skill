# Figures for NRF Proposals — TikZ Design Rules (추진체계도 · 간트차트 · 개념도)

> Adapted from the [`research-figure`](https://github.com/chingswy/Skill-Research-Figure) skill's
> TikZ approach. NRF reviewers are often senior and frequently print
> **2-up (두 쪽 모아찍기)**, so the #1 rule is: **large, bold, legible when shrunk.** Three figure
> types matter most; templates are in `templates/`.

## Design principles

1. **Legible when shrunk** — large fonts (≥ `\footnotesize`, prefer `\small`), thick arrows, high
   contrast. Test by viewing the PNG at 50% size.
2. **Card-based layout** — each module in a rounded rectangle; connect with clear arrows so the
   pipeline structure reads instantly.
3. **Low-saturation, professional palette** — muted blue/gray; never PowerPoint-vivid.
4. **Highlight the novel contribution** — the user's 창신 module gets a distinct fill / thicker
   border. This figure is literally arguing the 창의성 score.
5. **Sans-serif** (`\sffamily`) throughout; **Korean text** needs a Korean-capable engine (see below).
6. **Tie figures to the text** — the 추진체계도 mirrors the 세부목표 numbering in §2–3.

## Korean text in TikZ (important)

NRF figures contain Korean. Compile with **XeLaTeX or LuaLaTeX + a Korean font**, not pdflatex:

```latex
\documentclass[border=5pt]{standalone}
\usepackage{kotex} % or fontspec + \setmainfont{Noto Sans CJK KR}
\usepackage{tikz}
\usetikzlibrary{positioning,arrows.meta,fit,backgrounds,calc}
```

`scripts/compile_tikz.sh` auto-detects Korean (kotex/CJK) and falls back to xelatex/lualatex. If no
Korean font is installed, tell the user and offer to render labels in English/romanized or to
install `fonts-noto-cjk`.

## The three figure types

### 1. 추진체계도 (research framework / pipeline) — `templates/pipeline_diagram.tex`
Boxes-and-arrows showing how 세부목표/모듈 connect input → output. Highlight the novel module. Use
orthogonal routing (`|-`, `-|`, `rounded corners`) for non-aligned nodes — never diagonal lines.

### 2. 간트차트 (Gantt / 연차별 일정) — `templates/gantt_chart.tex`
The most-expected figure in 추진전략. Rows = 세부과제/세부목표, columns = 연차(분기), bars = duration,
diamonds = 마일스톤. Keep it tight; label each milestone.

### 3. 개념도 / 모식도 (concept figure)
For the core idea or the differentiation vs prior work (e.g. a 2-column "기존 연구 vs 본 연구"
visual). Often the single most persuasive object for the 창의성 score.

## Workflow (Phase 4)

1. Pick the template matching the need.
2. Fill in the user's modules / milestones / labels (in Korean).
3. Compile: `bash scripts/compile_tikz.sh <file.tex>` → produces cropped PDF + PNG.
4. **View the PNG** and self-check: readable at 50%? arrows correct? alignment clean? novel part
   highlighted? names match the text?
5. Iterate the `.tex`, recompile. **Never show a broken figure.**
6. Hand back the `.tex` (for `\input{}`) and a high-res PNG/PDF (most applicants paste into HWP/Word).

## Common pitfalls (from research-figure)

- **Diagonal arrows** between non-aligned nodes look amateur → orthogonal routing with `rounded
  corners` and `|-`/`-|`.
- **Duplicate node names** — only the last is reachable; use `\coordinate` for temp points.
- **`fit` node center offset** when children are asymmetric → use explicit anchors for arrows.
- **Text overflow** out of boxes → use `\\` line breaks and `text width=...`.
- **Korean shows as boxes/tofu** → wrong engine/font; use xelatex + kotex/Noto CJK KR.
