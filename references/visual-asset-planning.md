# Visual-Asset Planning — Tell the User *What* Image Goes *Where*

A fundable proposal is not just text. Reviewers skim, and figures carry disproportionate weight.
The skill must **plan the non-text elements**, not only write prose: for each section, say **what
kind of visual to place, where, and why it helps the score** — then either generate it (TikZ /
matplotlib) or leave a labeled placeholder for assets only the user can supply (lab photos, news
images, equipment shots).

## How the skill plans assets

While drafting (Phase 3) and in Phase 4, walk the sections and propose a small **asset plan**.
Each item: *위치 (which section) · 종류 (type) · 목적 (what it argues) · 출처/제작 (generate vs
user-supplied)*. Then drop a placeholder in the draft using the renderer's syntax:

```
::asset 4절 — 신청자 연구실의 드론/열화상 장비 사진. "수행역량"을 시각적으로 입증::
```

`scripts/write_hwpx.py` turns each `::asset …::` into a **[비주얼 자리] …** placeholder paragraph in
the `.hwpx`, so the user sees exactly where to paste what. Figures the skill *can* generate are
embedded directly with `![캡션](파일.png)`.

## Asset type → which tool / who supplies it

| Asset type (예) | Tool / source | Typical section |
|---|---|---|
| 추진체계도 / 파이프라인 (box-arrow) | **TikZ** (`templates/pipeline_diagram.tex`) — skill generates | 3. 추진체계 |
| 간트차트 / 연차별 일정 | **TikZ** (`templates/gantt_chart.tex`) — skill generates | 3-3 일정 |
| 성능 비교·추세·시장전망·TRL·레이더 (data charts) | **matplotlib** (`scripts/make_figure_mpl.py`) — skill generates | 1 예비결과, 4 차별성, 5 기대효과 |
| 개념도 / 모식도 (idea schematic) | TikZ or matplotlib — skill generates | 1 필요성, 2 내용 |
| **현장/뉴스 사진** (산불 현장, 피해 통계 인포그래픽) | **user-supplied** (placeholder + 출처·연도 명기 안내) | 1 필요성 도입 |
| **실험실 장비/셋업 사진** (드론, 열화상, 계측기) | **user-supplied** (placeholder) | 4 수행역량 |
| **예비결과 원본 이미지** (현미경/센서/스크린샷) | **user-supplied** (placeholder) | 1·4 |
| 기관 로고·조직도·협력체계 | user-supplied or simple TikZ | 3 추진체계, 글로벌 |

Rule of thumb: **skill generates anything synthesizable from numbers or structure**; **flags as a
placeholder anything that must be real-world (photos, news, proprietary screenshots)** — and never
fabricates a photo or a "result" image.

## Placement & quality guidance the skill should give

- **필요성 도입부:** a striking real photo or stat infographic earns the reviewer's attention in the
  first screen — recommend one, with **출처·연도 명기** (and source it via `web-source-finding.md`).
- **예비결과:** a data chart (matplotlib) that visibly shows your advantage beats a paragraph.
- **추진체계 + 일정:** the box-arrow framework and the Gantt are the two most-expected figures —
  generate both.
- **차별성/기대효과:** a comparison table or radar (matplotlib) makes the 창의성 case at a glance.
- **Legibility for 2-up printing:** large fonts, high contrast, highlight the novel module — see
  `figures-tikz.md` and `figures-matplotlib.md`.
- **Captions argue, not just label:** "그림 1. 멀티모달 융합이 야간·연기에서 큰 이득(예비결과)" —
  the caption states the takeaway.

## Output: an asset plan block (show the user)

```
[비주얼 자산 계획]
1. 필요성 도입 | 뉴스 사진/피해 인포그래픽 | 시급성 각인 | ▶ 사용자 제공(출처·연도)
2. 예비결과 | 막대 비교(matplotlib) | 악조건 이득 입증 | ▶ 자동생성(fig_perf.png)
3. 추진체계 | 파이프라인(TikZ) | 실행 구조 명료화 | ▶ 자동생성
4. 연차 일정 | 간트차트(TikZ) | 실행력 제시 | ▶ 자동생성
5. 수행역량 | 연구실 장비 사진 | 역량 시각 입증 | ▶ 사용자 제공
6. 차별성 | 레이더(matplotlib) | 우위 한눈에 | ▶ 자동생성
```
