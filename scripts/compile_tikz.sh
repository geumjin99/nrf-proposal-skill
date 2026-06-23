#!/usr/bin/env bash
# Compile a standalone TikZ figure to cropped PDF + PNG.
# Auto-detects Korean (kotex/CJK/fontspec) and uses xelatex; otherwise pdflatex.
# Usage: bash scripts/compile_tikz.sh <file.tex>
set -euo pipefail

TEX="${1:?usage: compile_tikz.sh <file.tex>}"
[ -f "$TEX" ] || { echo "ERROR: file not found: $TEX" >&2; exit 1; }
DIR="$(cd "$(dirname "$TEX")" && pwd)"
BASE="$(basename "$TEX" .tex)"
cd "$DIR"

# --- choose engine ---
ENGINE="pdflatex"
if grep -qiE '\\usepackage(\[[^]]*\])?\{(kotex|xeCJK|CJKutf8|fontspec)\}|setmainfont|Noto Sans CJK' "$BASE.tex"; then
  if   command -v xelatex  >/dev/null 2>&1; then ENGINE="xelatex"
  elif command -v lualatex >/dev/null 2>&1; then ENGINE="lualatex"
  else echo "WARN: Korean font engine (xelatex/lualatex) not found; trying pdflatex (한글 깨질 수 있음)." >&2; fi
fi
command -v "$ENGINE" >/dev/null 2>&1 || { echo "ERROR: $ENGINE not installed. Install TeX Live (e.g. 'sudo apt install texlive-xetex texlive-latex-extra texlive-lang-korean fonts-noto-cjk')." >&2; exit 1; }

echo ">> compiling $BASE.tex with $ENGINE"
"$ENGINE" -interaction=nonstopmode -halt-on-error "$BASE.tex" >/dev/null 2>"$BASE.log" || {
  echo "ERROR: compilation failed. Last log lines:" >&2; tail -n 25 "$BASE.log" >&2; exit 1; }

# --- PDF -> PNG (300 dpi) for quick viewing ---
if   command -v pdftoppm >/dev/null 2>&1; then
  pdftoppm -r 300 -png -singlefile "$BASE.pdf" "$BASE" && echo ">> PNG: $DIR/$BASE.png"
elif command -v magick  >/dev/null 2>&1; then
  magick -density 300 "$BASE.pdf" "$BASE.png" && echo ">> PNG: $DIR/$BASE.png"
elif command -v convert >/dev/null 2>&1; then
  convert -density 300 "$BASE.pdf" "$BASE.png" && echo ">> PNG: $DIR/$BASE.png"
else
  echo "NOTE: no pdftoppm/imagemagick; PDF only -> $DIR/$BASE.pdf" >&2
fi
echo ">> PDF: $DIR/$BASE.pdf"
# tidy aux files
rm -f "$BASE.aux" "$BASE.log" 2>/dev/null || true
