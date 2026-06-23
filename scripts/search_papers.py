#!/usr/bin/env python3
"""
search_papers.py — literature scout for the 국내외 연구 동향 section.

Queries free, no-key sources and merges/dedupes the results so every hit carries a
verifiable DOI/URL (anti-hallucination): OpenAlex (primary), Crossref, Semantic Scholar,
arXiv. Optionally checks open-access full text via Unpaywall.

Stdlib only — no pip install needed.

Usage:
    python3 scripts/search_papers.py "graph neural network protein interaction" \
        --email you@example.com --limit 12 --since 2021 [--oa] [--json]

For the Korean home-field layer (ScienceON / KCI / RISS / DBpia) you need API keys; see
references/academic-sources.md and use WebSearch/WebFetch or academic MCP tools instead.
"""
import argparse, json, sys, time, urllib.parse, urllib.request

UA = "nrf-proposal-skill/1.0 (mailto:%s)"

def _get(url, headers=None, timeout=25):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))

def _norm_title(t):
    return "".join(ch.lower() for ch in (t or "") if ch.isalnum())

# ---------- sources ----------
def openalex(q, limit, since, email):
    flt = f"&filter=from_publication_date:{since}-01-01" if since else ""
    url = (f"https://api.openalex.org/works?search={urllib.parse.quote(q)}"
           f"&per-page={limit}&sort=relevance_score:desc{flt}&mailto={email}")
    out = []
    for w in _get(url).get("results", []):
        ids = w.get("ids", {}) or {}
        out.append(dict(source="OpenAlex", title=w.get("title") or "",
                        year=w.get("publication_year"),
                        cites=w.get("cited_by_count", 0),
                        doi=(w.get("doi") or "").replace("https://doi.org/", "") or None,
                        venue=(((w.get("primary_location") or {}).get("source") or {}) or {}).get("display_name"),
                        url=ids.get("openalex"),
                        oa=(w.get("open_access") or {}).get("oa_url")))
    return out

def crossref(q, limit, email):
    url = (f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(q)}"
           f"&rows={limit}&select=title,DOI,issued,container-title,is-referenced-by-count&mailto={email}")
    out = []
    for it in _get(url).get("message", {}).get("items", []):
        yr = (((it.get("issued") or {}).get("date-parts") or [[None]])[0] or [None])[0]
        out.append(dict(source="Crossref",
                        title=(it.get("title") or [""])[0],
                        year=yr, cites=it.get("is-referenced-by-count", 0),
                        doi=it.get("DOI"),
                        venue=(it.get("container-title") or [None])[0],
                        url=("https://doi.org/" + it["DOI"]) if it.get("DOI") else None, oa=None))
    return out

def semanticscholar(q, limit):
    url = ("https://api.semanticscholar.org/graph/v1/paper/search?"
           f"query={urllib.parse.quote(q)}&limit={limit}"
           "&fields=title,year,citationCount,externalIds,venue,openAccessPdf,tldr")
    out = []
    try:
        data = _get(url)
    except Exception:
        time.sleep(2); data = _get(url) # gentle retry on rate limit
    for p in data.get("data", []) or []:
        ext = p.get("externalIds") or {}
        tldr = (p.get("tldr") or {}).get("text")
        out.append(dict(source="S2", title=p.get("title") or "", year=p.get("year"),
                        cites=p.get("citationCount", 0), doi=ext.get("DOI"),
                        venue=p.get("venue"),
                        url=("https://doi.org/" + ext["DOI"]) if ext.get("DOI")
                            else (f"https://arxiv.org/abs/{ext['ArXiv']}" if ext.get("ArXiv") else None),
                        oa=(p.get("openAccessPdf") or {}).get("url"), tldr=tldr))
    return out

def arxiv(q, limit):
    import xml.etree.ElementTree as ET
    url = (f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(q)}"
           f"&start=0&max_results={limit}&sortBy=relevance")
    req = urllib.request.Request(url, headers={"User-Agent": "nrf-proposal-skill"})
    with urllib.request.urlopen(req, timeout=25) as r:
        root = ET.fromstring(r.read())
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in root.findall("a:entry", ns):
        idu = (e.findtext("a:id", default="", namespaces=ns) or "")
        yr = (e.findtext("a:published", default="", namespaces=ns) or "")[:4]
        out.append(dict(source="arXiv",
                        title=" ".join((e.findtext("a:title", default="", namespaces=ns) or "").split()),
                        year=int(yr) if yr.isdigit() else None, cites=None,
                        doi=None, venue="arXiv (preprint, not peer-reviewed)",
                        url=idu, oa=idu))
    return out

def unpaywall(doi, email):
    try:
        d = _get(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={email}")
        loc = d.get("best_oa_location") or {}
        return loc.get("url_for_pdf") or loc.get("url")
    except Exception:
        return None

# ---------- merge ----------
def merge(rows):
    seen, out = {}, []
    for r in rows:
        key = r.get("doi") or _norm_title(r.get("title"))
        if not key:
            continue
        if key in seen:
            cur = seen[key]
            for f in ("doi", "venue", "url", "oa", "tldr", "cites", "year"):
                if not cur.get(f) and r.get(f):
                    cur[f] = r[f]
            cur["source"] = "+".join(sorted(set(cur["source"].split("+") + [r["source"]])))
        else:
            seen[key] = dict(r); out.append(seen[key])
    out.sort(key=lambda x: (x.get("cites") or -1), reverse=True)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--email", default="anonymous@example.com",
                    help="for OpenAlex/Crossref polite pool & Unpaywall (required by Unpaywall)")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--since", type=int, default=None, help="earliest publication year")
    ap.add_argument("--oa", action="store_true", help="resolve OA full text via Unpaywall")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = []
    for name, fn in (("OpenAlex", lambda: openalex(a.query, a.limit, a.since, a.email)),
                     ("Crossref", lambda: crossref(a.query, a.limit, a.email)),
                     ("S2", lambda: semanticscholar(a.query, a.limit)),
                     ("arXiv", lambda: arxiv(a.query, a.limit))):
        try:
            rows += fn()
        except Exception as e:
            print(f"[warn] {name} failed: {e}", file=sys.stderr)

    merged = merge(rows)[: a.limit]
    if a.oa:
        for r in merged:
            if r.get("doi") and not r.get("oa"):
                r["oa"] = unpaywall(r["doi"], a.email)

    if a.json:
        print(json.dumps(merged, ensure_ascii=False, indent=2)); return
    if not merged:
        print("No results. Try broader / English keywords.", file=sys.stderr); return
    for i, r in enumerate(merged, 1):
        c = "—" if r.get("cites") is None else r["cites"]
        print(f"{i:2}. [{r['source']}] ({r.get('year')}) cites={c} {r['title']}")
        if r.get("venue"): print(f" venue: {r['venue']}")
        if r.get("doi"): print(f" doi: https://doi.org/{r['doi']}")
        if r.get("url") and not r.get("doi"): print(f" url: {r['url']}")
        if r.get("oa"): print(f" OA: {r['oa']}")
        if r.get("tldr"): print(f" TLDR: {r['tldr']}")
    print(f"\n{len(merged)} works. Every entry has a resolvable link — cite only these; "
          "mark anything else [VERIFY].", file=sys.stderr)

if __name__ == "__main__":
    main()
