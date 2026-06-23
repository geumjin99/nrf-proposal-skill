# Data Figures with matplotlib (charts & concept visuals)

TikZ (`figures-tikz.md`) is for box-and-arrow 추진체계도 and 간트차트. **matplotlib** is for
**data-driven** figures — the kind that prove your point with numbers. Use `scripts/make_figure_mpl.py`.

## When to use matplotlib vs TikZ

| Use matplotlib | Use TikZ |
|---|---|
| 성능 비교 막대 (예비결과) | 추진체계도 / 파이프라인 |
| 추세선·예측, 시장규모 전망 | 간트차트 (연차별 일정) |
| TRL 로드맵, 레이더(차별성/역량) | 개념 도식(상자·화살표 위주) |
| 분포·산점도·히트맵 등 데이터 | |

## Korean fonts (the gotcha)

CJK fonts ship as `.ttc` and are **not** in matplotlib's name list, so a naive
`rcParams["font.family"]="Noto Sans CJK KR"` silently falls back to DejaVu → 한글이 □□ (tofu).
`make_figure_mpl.py` fixes this by resolving the font **file** via `fc-match` and registering it
with `fontManager.addfont()`, then using its real family name. If you write matplotlib code by hand:

```python
import subprocess, matplotlib.pyplot as plt
from matplotlib import font_manager as fm
path = subprocess.run(["fc-match","-f","%{file}","Noto Sans CJK KR"],
                      capture_output=True, text=True).stdout.strip()
fm.fontManager.addfont(path)
plt.rcParams["font.family"] = fm.FontProperties(fname=path).get_name()
plt.rcParams["axes.unicode_minus"] = False # 마이너스 깨짐 방지
```

## Usage — JSON spec in, figure out

```bash
python3 scripts/make_figure_mpl.py spec.json -o fig.png # or fig.pdf / fig.svg
echo '{...}' | python3 scripts/make_figure_mpl.py - -o fig.pdf
```

Supported `type`s (see the script's docstring for full schemas):

- **bar** — single-series comparison; `highlight` index draws "ours" in the accent color.
- **grouped** — multi-series grouped bars (기존 vs 제안 across conditions). *Verified example:
  화재 감지 성능 by 주간/야간/연기.*
- **line** — trends / forecasts (시장규모 전망); `annotate_last` labels the endpoints.
- **trl** — a left→right TRL roadmap of 연차 stages; last stage highlighted.
- **radar** — 차별성/역량 across axes (기존 최고 vs 제안), last series accented.

```json
{"type":"grouped","title":"화재 감지 성능 비교 (mAP)","ylabel":"mAP (%)",
 "x":["주간","야간","연기·역광"],
 "series":{"기존 RGB 단일":[82,49,38],"제안: 드론 멀티모달+AI":[90,84,79]}}
```

## Design rules (consistent with the TikZ figures)

- **Muted palette + one warm accent** for "ours"/novel (`#e6843c`); baselines in blue-gray.
- **Large, legible labels** (figures get printed 2-up) — keep titles bold, axes labeled with units.
- **Caption states the takeaway**, not just the variable: "그림 1. 멀티모달 융합이 야간·연기에서
  큰 이득(예비결과)."
- **Never fabricate data.** A chart is only as honest as its numbers — use the user's real
  preliminary results, or clearly mark illustrative/예시 values.
- Output **PDF** for the final document (vector), **PNG@300dpi** for previews; embed in the proposal
  with `![캡션](fig.png)` (the renderer absolutizes the path).

## Hand-off

Generated figures are embedded straight into the `.hwpx` by `write_hwpx.py` (reference them in the
draft with `![캡션](fig.png)`). Export PNG for embedding; a PDF/SVG copy is fine for the user's records.
