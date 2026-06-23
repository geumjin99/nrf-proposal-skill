#!/usr/bin/env python3
"""
write_hwpx.py — write a Korean proposal directly to a real HWP file (.hwpx), NO PDF.

.hwpx is the open, XML-based HWP format: Hancom Office opens it natively and can "다른 이름으로
저장 → .hwp". Native *binary* .hwp authoring needs Hancom's COM API (Windows), which isn't
available on open systems — so .hwpx is the correct, faithful output here. Built on python-hwpx
(`pip install python-hwpx`), which round-trips and validates the files it writes.

Converts a proposal Markdown into a styled .hwpx:
  # H1            -> centered title (bold)
  ## / ### / #### -> section headers (bold, graded sizes)
  paragraphs      -> body text, **bold** kept as bold runs
  - bullet        -> "· " bullet paragraph
  | md | table |  -> a real HWPX table (header row shaded)
  ![cap](img)     -> embedded picture + centered caption
  ::asset desc::  -> a bracketed "[비주얼 자리] …" placeholder paragraph (no emoji)

Usage:
  python3 scripts/write_hwpx.py draft.md -o out.hwpx [--title "..."]

The output is an editable HWP document — the deliverable. No PDF is produced.
"""
import argparse, os, re, sys, unicodedata

def nfc(s): return unicodedata.normalize("NFC", s)

def resolve(path):
    if os.path.exists(path): return path
    parts = os.path.normpath(path).split(os.sep); cur = os.sep if path.startswith(os.sep) else "."
    for seg in parts:
        if seg in ("", "."): continue
        nxt = os.path.join(cur, seg)
        if os.path.exists(nxt): cur = nxt; continue
        tgt = nfc(seg); m = None
        if os.path.isdir(cur):
            for f in os.listdir(cur):
                if nfc(f) == tgt: m = os.path.join(cur, f); break
        if m is None: raise FileNotFoundError(f"cannot resolve '{seg}' in {path}")
        cur = m
    return cur

HEADING_SIZE = {1: 16, 2: 13, 3: 11.5, 4: 10.5}

def add_runs(para, text):
    """Add text to a paragraph, rendering **bold** segments as bold runs; strip `code`/* markers."""
    text = text.replace("`", "")
    parts = re.split(r'(\*\*.+?\*\*)', text)
    for seg in parts:
        if not seg: continue
        if seg.startswith("**") and seg.endswith("**"):
            para.add_run(seg[2:-2], bold=True)
        else:
            seg = re.sub(r'(?<!\*)\*(?!\*)', '', seg)  # drop stray single * (italic markers)
            para.add_run(seg)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--title", default=None)
    a = ap.parse_args()
    try:
        from hwpx.document import HwpxDocument
    except ImportError:
        sys.exit("ERROR: python-hwpx not installed. Run: pip install python-hwpx")

    src = resolve(a.md)
    base_dir = os.path.dirname(os.path.abspath(src))
    out = os.path.abspath(a.out or os.path.splitext(os.path.basename(src))[0] + ".hwpx")
    lines = open(src, encoding="utf-8").read().splitlines()

    doc = HwpxDocument.new()
    try:
        doc.set_page_margins(left=20*283//10, right=20*283//10, top=20*283//10, bottom=18*283//10)
    except Exception:
        pass  # margins are nice-to-have; HWPUNIT≈283/mm

    def align_last(alignment):
        # Set alignment EXPLICITLY on every paragraph. python-hwpx's add_paragraph
        # inherits the previous paragraph's style by default, so without this a single
        # centered title would bleed "center" onto every following paragraph.
        try: doc.set_paragraph_format(paragraph_index=len(doc.paragraphs)-1, alignment=alignment)
        except Exception: pass

    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]; s = ln.strip()
        # --- asset placeholder ---
        m = re.match(r'^::asset\s+(.+?)::\s*$', s)
        if m:
            p = doc.add_paragraph("")
            p.add_run("[비주얼 자리] ", bold=True)
            p.add_run(m.group(1).strip() + "  (실제 이미지/사진/도표를 이 위치에 삽입)")
            align_last("left"); i += 1; continue
        # --- image ---
        m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', s)
        if m:
            cap, path = m.group(1), m.group(2).strip()
            ip = path if os.path.isabs(path) else os.path.join(base_dir, path)
            try:
                ip = resolve(ip)
                fmt = os.path.splitext(ip)[1].lstrip(".").lower() or "png"
                with open(ip, "rb") as fh: data = fh.read()
                doc.add_picture(data, fmt, width_mm=150, align="center")
            except Exception as e:
                p = doc.add_paragraph(""); p.add_run(f"[그림 누락: {path} — {e}]", bold=True)
                align_last("left")
            if cap:
                doc.add_paragraph(cap); align_last("center")
            i += 1; continue
        # --- table (consecutive | ... | lines) ---
        if s.startswith("|") and s.endswith("|"):
            block = []
            while i < n and lines[i].strip().startswith("|"):
                block.append(lines[i].strip()); i += 1
            rows = [[c.strip() for c in r.strip("|").split("|")] for r in block]
            rows = [r for r in rows if not all(re.fullmatch(r'\s*:?-+:?\s*', c) for c in r)]  # drop --- sep
            if rows:
                ncol = max(len(r) for r in rows)
                t = doc.add_table(len(rows), ncol)
                for ri, r in enumerate(rows):
                    for ci in range(ncol):
                        txt = r[ci] if ci < len(r) else ""
                        txt = txt.replace("**", "")
                        try: t.set_cell_text(ri, ci, txt)
                        except Exception: pass
                    if ri == 0:
                        for ci in range(ncol):
                            try: t.set_cell_shading(0, ci, "ECECEC")
                            except Exception: pass
            continue
        # --- heading ---
        m = re.match(r'^(#{1,4})\s+(.*)$', s)
        if m:
            lvl = len(m.group(1)); txt = m.group(2).strip()
            p = doc.add_paragraph("")
            p.add_run(txt, bold=True, size=HEADING_SIZE.get(lvl, 11))
            align_last("center" if lvl == 1 else "left")
            i += 1; continue
        # --- bullet ---
        m = re.match(r'^[-*]\s+(.*)$', s)
        if m:
            p = doc.add_paragraph(""); p.add_run("· "); add_runs(p, m.group(1)); align_last("left"); i += 1; continue
        # --- blank ---
        if not s:
            i += 1; continue
        # --- horizontal rule ---
        if re.fullmatch(r'-{3,}', s):
            i += 1; continue
        # --- normal paragraph ---
        p = doc.add_paragraph(""); add_runs(p, s); align_last("justify"); i += 1

    doc.save_to_path(out)
    # verify round-trip
    try:
        chk = HwpxDocument.open(out)
        rep = chk.validate() if hasattr(chk, "validate") else None
        issues = getattr(rep, "issues", ()) if rep else ()
        nchars = len(chk.export_text())
        print(f"HWPX: {out} ({os.path.getsize(out)} bytes) — validated, {len(issues)} issues, "
              f"{nchars} chars readable")
    except Exception as e:
        print(f"HWPX: {out} ({os.path.getsize(out)} bytes) — written (verify warn: {e})")

if __name__ == "__main__":
    main()
