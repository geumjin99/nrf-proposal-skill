# HWP / HWPX Handling — Read the Template, Write the Proposal as HWP

Korean grant paperwork lives in **HWP** (한글, Hancom Office). This skill (a) **reads** the user's
existing `.hwp` — the official 양식, an RFP/공고, a sample — and (b) **writes the proposal as a real
HWP file (`.hwpx`)**. The deliverable is HWP, not PDF.

> Read with `scripts/hwp_tools.py`. Write with `scripts/write_hwpx.py`. Everything below was
> verified on real files on this machine.

---

## 0. The #1 gotcha: Korean filenames (NFC vs NFD)

Korean filenames on disk are frequently **NFD-normalized** (decomposed jamo), while a path you
*type or paste* is **NFC** (composed). They look identical but are different bytes, so
`open()`/`cd`/glob raise `FileNotFoundError` **even though `find` lists the file** — and the trap
hits **directory** components too, not just the filename.

- Fix: resolve paths by matching real on-disk bytes, NFC/NFD-insensitively. Both `hwp_tools.py`
  and `write_hwpx.py` do this in `resolve()` (segment by segment). When scripting by hand,
  enumerate with `os.listdir()`/`os.walk()` comparing `unicodedata.normalize("NFC", name)`, or use
  `find <dir> -name '*.hwp' -exec <cmd> {} \;`.
- Always discover files with `python3 scripts/hwp_tools.py find <dir> [substr]`.

---

## 1. Reading `.hwp` (intake) — verified

Toolchain: **pyhwp** (`hwp5txt`, `hwp5html`). Install: `pip install pyhwp`.

| Need | Command | Notes (verified) |
|---|---|---|
| Body text | `hwp_tools.py text <f>` | Clean Korean prose. **Tables render as `<표>` placeholders** — a table-heavy 양식 yields little text. |
| Structure + tables | `hwp_tools.py html <f>` | `index.xhtml` + `styles.css`; tables/layout preserved (the `styles.css` even lists the template's fonts: 바탕/명조/굴림/한양신명조 …). |
| Tables as TSV | `hwp_tools.py tables <f>` | Real cell contents (verified on the drone RFP: 품목명, TRL, 분류). |

So: prose docs → `text`; 양식/RFP/표 많은 문서 → `html` or `tables`. Use this in **Phase 0** to match
the draft to the real section labels and tables.

`.hwpx` (newer OWPML format) is a ZIP of XML; read it with `python-hwpx` (`HwpxDocument.open(...)`
→ `.export_text()` / `.get_table_map()`), or unzip and parse `Contents/section*.xml`.

---

## 2. Writing the proposal as HWP — `.hwpx` (the deliverable, no PDF)

**Reality:** native *binary* `.hwp` authoring needs Hancom's COM API (Windows + Hancom installed),
unavailable on open systems. The correct, faithful output is **`.hwpx`** — the open, XML-based HWP
format that **Hancom Office opens natively** and can re-save as `.hwp` (다른 이름으로 저장 → .hwp).
We do **not** convert to PDF.

Built on **python-hwpx** (`pip install python-hwpx`), which round-trips and `validate()`s its output.

```
scripts/write_hwpx.py <draft.md> -o out.hwpx [--title "..."]
```

Markdown → styled `.hwpx`:
- `# H1` → centered title (bold); `##`/`###`/`####` → section headers (bold, graded sizes)
- paragraphs with `**bold**` kept as bold runs; `- ` → "· " bullets
- `| md | table |` → a **real HWPX table** (header row shaded)
- `![cap](img.png)` → **embedded picture** (width 150 mm) + centered caption
- `::asset 설명::` → a bracketed `[비주얼 자리] 설명` placeholder paragraph (no emoji)

*Verified:* drone+AI-fire demo → `제안서_드론화재.hwpx`, **validate() 0 issues**, 3 figures embedded
(`BinData/BIN0001-3.png`), text reads back via `export_text()`.

### Fonts — why this is now correct
When the `.hwpx` is opened in Hancom, it renders with **Hancom's own fonts** (함초롬바탕 등). There is
no PDF conversion and no font substitution, so the earlier "글꼴이 틀리다 / generic-LaTeX look"
problem does not arise. To set a specific body font in the file, pass run/style attributes via
python-hwpx (e.g. `ensure_run_style(font="함초롬바탕")`); if that font is installed it is used, else
Hancom substitutes on open.

### Filling an official template
If the user has an official **`.hwpx`** 양식, fill it in place with python-hwpx
(`HwpxDocument.open(form).fill_form_field(...)` / `find_cell_by_label(...)` / `set_cell_text(...)`)
and save — preserving the form exactly. If the official form is **binary `.hwp`**, ask the user to
"다른 이름으로 저장 → .hwpx" in Hancom once, then fill the `.hwpx`; or author a fresh `.hwpx` with
`write_hwpx.py` matching the form's section labels (read via `hwp_tools.py text|tables`).

---

## 3. Dependencies

| Capability | Tool | Install |
|---|---|---|
| Read .hwp | pyhwp | `pip install pyhwp` |
| Write .hwpx (deliverable) | python-hwpx | `pip install python-hwpx` |
| Figures to embed (PNG) | matplotlib / TikZ | see `figures-matplotlib.md`, `figures-tikz.md` |

`write_hwpx.py` and `hwp_tools.py` report the missing tool and how to install it if absent — they
never silently produce a broken file.

---

## 4. Where this plugs into the workflow

- **Phase 0 (intake):** `find` + `text`/`tables`/`html` to read the official 양식, the 공고/RFP, and
  any sample — so the draft matches the real section labels and table structures.
- **Phase 4 (figures):** generate PNGs (matplotlib/TikZ) to embed.
- **Phase 6 (deliver):** `write_hwpx.py` → `.hwpx`. Tell the user it opens in Hancom and can be
  saved as `.hwp`; remind them to replace every `[비주얼 자리]`/`[TODO]`/`[VERIFY]`, and that the
  text must become their own (responsible-use stance).
