#!/usr/bin/env python3
"""
make_figure_mpl.py — matplotlib figures for NRF proposals (data charts & concept visuals),
complementing the TikZ pipeline/Gantt figures. Korean labels render via Noto Sans CJK KR.

Use matplotlib (not TikZ) when the figure is DATA-driven or chart-like:
  성능 비교 막대, 추세선/예측, 시장규모 전망, TRL 로드맵, 레이더(역량/차별성) 등.
Use TikZ (templates/*.tex) for box-and-arrow 추진체계도 and 간트차트.

Drive it with a JSON spec (file path or stdin):
  python3 scripts/make_figure_mpl.py spec.json -o fig.png
  echo '{...}' | python3 scripts/make_figure_mpl.py - -o fig.pdf

Spec schema (type-specific):
  {"type":"bar","title":"성능 비교","ylabel":"정확도(%)",
   "x":["기존A","기존B","제안(Ours)"],"y":[71,76,89],"highlight":2}
  {"type":"grouped","title":"...","ylabel":"mAP","x":["주간","야간","연기"],
   "series":{"기존":[80,55,40],"제안":[88,79,72]}}
  {"type":"line","title":"시장 규모 전망","xlabel":"연도","ylabel":"억원",
   "x":[2024,2025,2026,2027,2028],"series":{"국내":[120,150,190,240,310]},"annotate_last":true}
  {"type":"trl","title":"TRL 추진 로드맵","stages":[["1차년","TRL3→4","개념·예비"],
   ["2차년","TRL4→5","핵심기법"],["3차년","TRL5→6","실증"]]}
  {"type":"radar","title":"연구 차별성","axes":["정확도","실시간성","견고성","해석성","비용"],
   "series":{"기존 최고":[7,5,4,3,6],"제안":[9,8,8,7,7]},"max":10}

Deps: matplotlib (+ Noto CJK fonts). Output by extension: .png (300dpi) / .pdf / .svg.
"""
import json, sys, argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# ---- Korean font ----
def _set_korean_font():
    """CJK fonts ship as .ttc and aren't in matplotlib's name list; resolve the file via
    fontconfig, register it, and use its real family name. Falls back gracefully."""
    import subprocess
    plt.rcParams["axes.unicode_minus"] = False
    for query in ("Noto Sans CJK KR", "NanumGothic", "Baekmuk Dotum", "UnDotum", "sans-serif:lang=ko"):
        try:
            path = subprocess.run(["fc-match", "-f", "%{file}", query],
                                  capture_output=True, text=True).stdout.strip()
        except Exception:
            path = ""
        if path and path.lower().endswith((".ttf", ".otf", ".ttc")):
            try:
                fm.fontManager.addfont(path)
                name = fm.FontProperties(fname=path).get_name()
                plt.rcParams["font.family"] = name
                return name
            except Exception:
                continue
    return None
_KFONT = _set_korean_font()

ACCENT = "#e6843c"; BASE = "#90a4ae"; INK = "#37474f"
PALETTE = ["#90a4ae", "#5c9bd1", "#7bb274", "#e6843c", "#b07bc4"]

def _finish(fig, out):
    fig.tight_layout()
    dpi = 300 if out.lower().endswith(".png") else None
    fig.savefig(out, dpi=dpi, bbox_inches="tight", transparent=False)
    print(f"FIG: {out}")

def bar(s, out):
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    hi = s.get("highlight")
    colors = [ACCENT if i == hi else BASE for i in range(len(s["x"]))]
    bars = ax.bar(s["x"], s["y"], color=colors, edgecolor=INK, linewidth=0.6)
    for b, v in zip(bars, s["y"]):
        ax.text(b.get_x()+b.get_width()/2, v, f"{v}", ha="center", va="bottom", fontsize=9)
    ax.set_ylabel(s.get("ylabel", "")); ax.set_title(s.get("title", ""), fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    _finish(fig, out)

def grouped(s, out):
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    cats = s["x"]; series = s["series"]; n = len(series); w = 0.8/n
    import numpy as np
    xpos = np.arange(len(cats))
    for i, (name, vals) in enumerate(series.items()):
        off = (i-(n-1)/2)*w
        ax.bar(xpos+off, vals, w, label=name, color=PALETTE[i % len(PALETTE)],
               edgecolor=INK, linewidth=0.5)
    ax.set_xticks(xpos); ax.set_xticklabels(cats)
    ax.set_ylabel(s.get("ylabel", "")); ax.set_title(s.get("title", ""), fontweight="bold")
    ax.legend(frameon=False, fontsize=9); ax.spines[["top", "right"]].set_visible(False)
    _finish(fig, out)

def line(s, out):
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    for i, (name, vals) in enumerate(s["series"].items()):
        ax.plot(s["x"], vals, marker="o", color=PALETTE[i % len(PALETTE)], label=name, linewidth=2)
        if s.get("annotate_last"):
            ax.annotate(f"{vals[-1]}", (s["x"][-1], vals[-1]), textcoords="offset points",
                        xytext=(4, 4), fontsize=9, color=PALETTE[i % len(PALETTE)])
    ax.set_xlabel(s.get("xlabel", "")); ax.set_ylabel(s.get("ylabel", ""))
    ax.set_title(s.get("title", ""), fontweight="bold")
    if len(s["series"]) > 1: ax.legend(frameon=False, fontsize=9)
    ax.grid(alpha=0.3); ax.spines[["top", "right"]].set_visible(False)
    _finish(fig, out)

def trl(s, out):
    stages = s["stages"]; n = len(stages)
    fig, ax = plt.subplots(figsize=(1.9*n+0.6, 2.4)); ax.axis("off")
    for i, st in enumerate(stages):
        x = i*1.9
        c = ACCENT if i == n-1 else "#5c9bd1"
        ax.add_patch(plt.Rectangle((x, 0.2), 1.5, 1.4, fc=c, ec=INK, lw=0.8, alpha=0.85,
                                   joinstyle="round"))
        yr, trl_, desc = (st + ["", "", ""])[:3]
        ax.text(x+0.75, 1.32, yr, ha="center", fontsize=10, fontweight="bold", color="white")
        ax.text(x+0.75, 0.95, trl_, ha="center", fontsize=10, color="white")
        ax.text(x+0.75, 0.5, desc, ha="center", fontsize=8.5, color="white")
        if i < n-1:
            ax.annotate("", xy=(x+1.85, 0.9), xytext=(x+1.5, 0.9),
                        arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.5))
    ax.set_xlim(-0.1, 1.9*n); ax.set_ylim(0, 2)
    ax.set_title(s.get("title", ""), fontweight="bold", fontsize=12)
    _finish(fig, out)

def radar(s, out):
    import numpy as np
    axes = s["axes"]; N = len(axes); mx = s.get("max", 10)
    ang = np.linspace(0, 2*np.pi, N, endpoint=False).tolist(); ang += ang[:1]
    fig, ax = plt.subplots(figsize=(4.4, 4.0), subplot_kw=dict(polar=True))
    for i, (name, vals) in enumerate(s["series"].items()):
        v = vals + vals[:1]
        c = ACCENT if i == len(s["series"])-1 else PALETTE[i % len(PALETTE)]
        ax.plot(ang, v, color=c, linewidth=2, label=name)
        ax.fill(ang, v, color=c, alpha=0.15)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(axes, fontsize=9)
    ax.set_ylim(0, mx); ax.set_yticklabels([])
    ax.set_title(s.get("title", ""), fontweight="bold", pad=16)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), frameon=False, fontsize=9)
    _finish(fig, out)

KINDS = {"bar": bar, "grouped": grouped, "line": line, "trl": trl, "radar": radar}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", help="JSON spec file, or '-' for stdin")
    ap.add_argument("-o", "--out", required=True, help="output .png/.pdf/.svg")
    a = ap.parse_args()
    raw = sys.stdin.read() if a.spec == "-" else open(a.spec, encoding="utf-8").read()
    spec = json.loads(raw)
    kind = spec.get("type")
    if kind not in KINDS:
        sys.exit(f"unknown type '{kind}'. options: {', '.join(KINDS)}")
    KINDS[kind](spec, a.out)

if __name__ == "__main__":
    main()
