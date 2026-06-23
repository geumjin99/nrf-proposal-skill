# Search Sources & API Cheatsheet — International + Korean + Market

> Two layers are mandatory for an NRF proposal: an **international** frontier layer and a **Korean
> home-field** layer (you must show domestic 연구 현황). A **market/industry** layer is needed for
> 사업화 / 기대효과 sections. Free, no-key sources are the skill's defaults.

---

## A. International (default main layer — free, no key)

| Source | Coverage | API | Best for |
|---|---|---|---|
| **OpenAlex** | 250M+ works, all fields; aggregates Crossref/ORCID/Unpaywall | `https://api.openalex.org/works?search=...&mailto=EMAIL` — no key | Primary search, citation counts, author/venue/concept stats, trend stats (~98.6% coverage) |
| **Semantic Scholar** | 200M+ papers, strong CS/AI | `https://api.semanticscholar.org/graph/v1/paper/search` — free, optional key for higher limits | High-cited, TLDR summaries, citation graph, recommendations |
| **Crossref** | 150M+ DOI records | `https://api.crossref.org/works?query=...&mailto=EMAIL` — no key | DOI metadata, venue/publisher, completing references |
| **arXiv** | STEM preprints | `http://export.arxiv.org/api/query?search_query=...` — public | Frontier, unpublished (mark "not peer-reviewed") |
| **Unpaywall** | OA availability | `https://api.unpaywall.org/v2/{DOI}?email=EMAIL` — 100k/day | Is there a legal OA full text? get the PDF link |
| **PubMed E-utilities** | biomedical/life science | free (key speeds up) | medical / life-science trends |
| Google Scholar | broadest, incl. grey lit | **no official API** (blocks scrapers) | manual cross-check only — do NOT automate |

`scripts/search_papers.py` wraps OpenAlex + Crossref + Semantic Scholar + arXiv + Unpaywall.

## B. Korean home-field (mandatory for 국내 연구 현황)

| Source | Operator / coverage | API | Best for |
|---|---|---|---|
| **ScienceON (KISTI)** | national S&T infra; 123M+ papers, 44M+ patents, 395k+ reports | API Gateway, **needs key**: https://scienceon.kisti.re.kr/por/oapi/openApi.do | **First choice for Korean STEM 동향** — papers + patents + national R&D reports in one |
| **NDSL (KISTI)** | ScienceON's predecessor services | REST OpenAPI | mashup with ScienceON |
| **KCI (NRF-run)** | Korea Citation Index — journal-tier authority | OpenAPI via data.go.kr "KCI 논문정보서비스": https://www.data.go.kr/data/15085348/openapi.do | **journal-tier (KCI 등재) judgment**, domestic citation/trend stats |
| **DBpia** | commercial; domestic journals/conferences | Open API (자료유형 1=학술지/2=학회/3=전문잡지/4=연구보고서): https://api.dbpia.co.kr/openApi/about/search.do | domestic full-text supplement |
| **RISS (KERIS)** | theses + integrated resources | RISS API 센터 (register via ScienceON) | **Korean master's/PhD theses** (domestic 동향) |
| **KISS** | commercial; strong humanities/social | mostly institutional | 인문사회 supplement |

Most Korean sources need a key — when the script can't reach them, use `WebSearch`/`WebFetch` or
the connected academic MCP tools and verify each hit has a resolvable link.

## C. Market / industry (for 사업화 · 기대효과 · PART2 §5)

| Source | Content | Link |
|---|---|---|
| **KOSIS 국가통계포털** | national approved statistics (一手 data) | https://kosis.kr/ |
| **KIET 산업연구원** | 산업동향 브리프, 주요산업 지표 (authoritative 二手, free) | https://www.kiet.re.kr/trends/indbriefList |
| **KISTI KMAPS** | 산업·시장 규모/전망, 시장집중도 | https://kmapsneo.kisti.re.kr/stat/statisticAnal.do |
| **KISTEP 기술동향 브리프** | tech trends, future-tech foresight (二手) | via ScienceON |
| **KIPRIS / KIPRIS Plus** | Korean patent full-text; patent-trend metrics | https://www.kipris.or.kr/ ; API https://plus.kipris.or.kr (free 1,000/mo) |
| Statista / Gartner / IDC / OECD / IEA | global market/policy (二手, often paid) | cite public summaries with year, verify |

> Patent metrics (KIPRIS) are great quantifiable 一手 evidence for 기술/산업 동향 — show filing
> trends, main IPC classes, main applicants to back up "this tech is hot."

---

## Quick API recipes (no key)

```bash
# OpenAlex — top works by relevance, with citation counts
curl 'https://api.openalex.org/works?search=graph%20neural%20network%20protein&per-page=10&mailto=YOU@EMAIL'

# Crossref — resolve/complete a reference
curl 'https://api.crossref.org/works?query.bibliographic=attention+is+all+you+need&rows=3&mailto=YOU@EMAIL'

# Semantic Scholar — search with fields
curl 'https://api.semanticscholar.org/graph/v1/paper/search?query=protein+interaction+GNN&fields=title,year,citationCount,externalIds,tldr'

# Unpaywall — is there an OA full text?
curl 'https://api.unpaywall.org/v2/10.1038/nature14539?email=YOU@EMAIL'
```

Replace `YOU@EMAIL` with the user's email (polite-pool / required by Unpaywall). The bundled
`scripts/search_papers.py` does all of this and merges/dedupes results.
