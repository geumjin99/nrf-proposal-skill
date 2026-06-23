#!/usr/bin/env python3
"""
hwp_tools.py — READ Korean HWP/HWPX documents (intake of the user's 양식 / 공고 / sample).

This script only READS. To WRITE the proposal as a real HWP file, use `write_hwpx.py` (.hwpx).

  .hwp --hwp5txt--> body text (tables show as <표>; use html/tables for table-heavy docs)
  .hwp --hwp5html--> XHTML+CSS (preserves tables/structure)

Why this script exists instead of calling hwp5txt directly:
  * Korean filenames on disk are often NFD-normalized; a path you *type* (NFC) won't match,
    raising FileNotFoundError even though `find` lists the file. This resolves files by
    matching real on-disk bytes (NFC/NFD-insensitive) so it "just works".

Subcommands:
  find <dir> [substr]  list .hwp/.hwpx under dir (NFC/NFD-safe), optional name filter
  text <file>          extract body text (hwp5txt)
  html <file> [outdir] convert to XHTML+CSS (hwp5html) — best for tables/structure
  tables <file>        extract tables as TSV (from the hwp5html render)

Deps: pyhwp (hwp5txt/hwp5html).
"""
import os, sys, subprocess, unicodedata, glob, shutil, tempfile

def _nfkey(s):
    return unicodedata.normalize("NFC", s)

def resolve(path):
    """Resolve a path whose Korean components may differ in NFC/NFD normalization.

    Walks the path segment by segment so a *typed* (usually NFC) path still matches
    on-disk names (often NFD), for BOTH directory and file components.
    """
    if os.path.exists(path):
        return path
    parts = os.path.normpath(path).split(os.sep)
    cur = os.sep if path.startswith(os.sep) else "."
    for seg in parts:
        if seg in ("", "."):
            continue
        nxt = os.path.join(cur, seg)
        if os.path.exists(nxt):
            cur = nxt; continue
        target = _nfkey(seg)
        match = None
        if os.path.isdir(cur):
            for f in os.listdir(cur):
                if _nfkey(f) == target:
                    match = os.path.join(cur, f); break
        if match is None:
            raise FileNotFoundError(f"cannot resolve (NFC/NFD-safe) segment '{seg}' in: {path}")
        cur = match
    return cur

def need(tool):
    if shutil.which(tool) is None:
        sys.exit(f"ERROR: '{tool}' not installed. See references/hwp-handling.md for install hints.")

def cmd_find(args):
    base = args[0] if args else "."
    sub = _nfkey(args[1]) if len(args) > 1 else None
    hits = []
    for root, _, files in os.walk(base):
        for f in files:
            if f.lower().endswith((".hwp", ".hwpx")):
                if sub is None or sub in _nfkey(f):
                    hits.append(os.path.join(root, f))
    for h in sorted(hits):
        print(h)
    print(f"\n{len(hits)} file(s).", file=sys.stderr)

def cmd_text(args):
    need("hwp5txt")
    src = resolve(args[0])
    r = subprocess.run(["hwp5txt", src], capture_output=True, text=True)
    if r.returncode:
        sys.exit("hwp5txt failed: " + (r.stderr.strip()[-200:] or "unknown"))
    out = r.stdout
    if out.count("<표>") > 5 and len(out.strip()) < 200:
        print("[hint] this doc is table-heavy; hwp5txt shows <표> placeholders — "
              "use `html` or `tables` instead.", file=sys.stderr)
    sys.stdout.write(out)

def _to_html(src, outdir):
    need("hwp5html")
    os.makedirs(outdir, exist_ok=True)
    r = subprocess.run(["hwp5html", "--output", outdir, src], capture_output=True, text=True)
    if r.returncode:
        sys.exit("hwp5html failed: " + (r.stderr.strip()[-200:] or "unknown"))
    xhtml = os.path.join(outdir, "index.xhtml")
    if not os.path.exists(xhtml):
        sys.exit("hwp5html produced no index.xhtml")
    return xhtml

def cmd_html(args):
    src = resolve(args[0])
    outdir = args[1] if len(args) > 1 else os.path.splitext(os.path.basename(src))[0] + "_html"
    xhtml = _to_html(src, outdir)
    print(xhtml)

def cmd_tables(args):
    src = resolve(args[0])
    tmp = tempfile.mkdtemp(prefix="hwp_")
    xhtml = _to_html(src, tmp)
    try:
        from html.parser import HTMLParser
    except Exception:
        sys.exit("stdlib html.parser unavailable")

    class T(HTMLParser):
        def __init__(s):
            super().__init__(); s.tables=[]; s.row=None; s.cell=None; s.intd=False
        def handle_starttag(s, tag, attrs):
            if tag=="table": s.tables.append([])
            elif tag=="tr" and s.tables: s.row=[]
            elif tag in ("td","th") and s.row is not None: s.cell=""; s.intd=True
        def handle_endtag(s, tag):
            if tag in ("td","th") and s.intd: s.row.append(" ".join(s.cell.split())); s.intd=False
            elif tag=="tr" and s.row is not None and s.tables: s.tables[-1].append(s.row); s.row=None
        def handle_data(s, data):
            if s.intd: s.cell += data
    p = T()
    p.feed(open(xhtml, encoding="utf-8").read())
    if not p.tables:
        print("(no tables found)", file=sys.stderr); return
    for i, tb in enumerate(p.tables, 1):
        print(f"# --- table {i} ({len(tb)} rows) ---")
        for row in tb:
            print("\t".join(row))
        print()
    shutil.rmtree(tmp, ignore_errors=True)

CMDS = {"find": cmd_find, "text": cmd_text, "html": cmd_html, "tables": cmd_tables}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__); sys.exit(0 if len(sys.argv) < 2 else 2)
    CMDS[sys.argv[1]](sys.argv[2:])

if __name__ == "__main__":
    main()
