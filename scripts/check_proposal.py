#!/usr/bin/env python3
"""
check_proposal.py — pre-submission gate for an NRF 연구계획서 draft (Phase 6).

Heuristic checks (text/markdown in, findings out):
  - page-budget estimate vs the program limit (overflow is NOT reviewed)
  - leftover placeholders ([TODO]/[VERIFY]/[PLACEHOLDER]/[수치]/[기관명])
  - hype words reviewers dislike (과장·허세)
  - undefined acronyms (ALL-CAPS / Latin acronyms used before being spelled out)
  - over-emphasis (too much **bold**)
  - blind-review identity leaks (--blind: names, institutions, self-citation)
  - missing 참고문헌 / citations

This is a lint, not a verdict. It cannot judge scientific quality — that's Phase 5.

Usage:
    python3 scripts/check_proposal.py draft.md --program sinjin [--blind]
    programs: sinjin(10p) | haeksim(10p) | haeksimA(5p) | hanwoomul(7p) | sejong(10p) | humanities
"""
import argparse, re, sys

PAGE_LIMIT = {"sinjin": 10, "haeksim": 10, "haeksimA": 5, "hanwoomul": 7,
              "sejong": 10, "humanities": None}
# rough chars/page for a Korean A4 proposal body (10pt, ~15mm margins). Heuristic only.
CHARS_PER_PAGE = 1800

PLACEHOLDERS = [r"\[TODO\]", r"\[VERIFY[^\]]*\]", r"\[PLACEHOLDER\]", r"\[수치\]",
                r"\[기관명\]", r"\[\s*\]", r"\bTBD\b", r"XXX+"]
HYPE = ["세상을 바꾸", "혁명적", "획기적으로 모든", "최초이자 유일", "학계를 뒤흔들",
        "세계 최고 수준의 독보적", "반드시 성공", "전무후무", "그 누구도",
        "world-changing", "revolutionary breakthrough", "first and only ever"]
SELF_CITE = [r"본\s*연구자(의|는)", r"저자(의|는)\s*선행", r"신청자(의|는)\s*기존",
             r"our previous work", r"we previously (showed|developed)"]

def find_emoji(body):
    # emoji / decorative pictographs that must NOT appear in a formal proposal
    # (keeps typographic arrows and box drawing; flags 1F* pictographs and misc symbol ranges)
    rng = [(0x1F000,0x1FAFF),(0x2600,0x26FF),(0x2700,0x27BF),(0x2B00,0x2BFF),
           (0x2705,0x2705),(0x274C,0x274C),(0xFE00,0xFE0F),(0x2728,0x2728)]
    return sorted({ch for ch in body if any(a<=ord(ch)<=b for a,b in rng)})

def estimate_pages(body):
    # count visible chars excluding markdown noise & the 참고문헌/실적 (page-exempt) tail
    cut = re.split(r"(?m)^#+\s*(참고문헌|references|대표적?\s*연구실적)", body, maxsplit=1)[0]
    text = re.sub(r"[#*`>\-\|\[\]]", "", cut)
    text = re.sub(r"\s+", "", text)
    return len(text) / CHARS_PER_PAGE, len(text)

def find_acronyms(body):
    # acronyms = 2-6 Latin uppercase letters; flag if first occurrence has no '(' nearby (spell-out)
    flagged = {}
    for m in re.finditer(r"\b([A-Z]{2,6})\b", body):
        ac = m.group(1)
        if ac in ("AI", "DNA", "RNA", "PI", "ID", "OK", "NRF", "IRIS"): # common/whitelisted
            continue
        if ac in flagged:
            continue
        window = body[max(0, m.start() - 60): m.start()]
        # spelled out if a '(' precedes it within the window (e.g. "... (CNN)")
        if "(" + ac not in body[max(0, m.start()-1):m.start()+len(ac)+1] and \
           not re.search(r"[A-Za-z가-힣]\s*\(\s*$", window):
            flagged[ac] = m.start()
    return flagged

def report(title, items, ok_msg, fmt=lambda x: x, limit=12):
    print(f"\n### {title}")
    if not items:
        print(f" {ok_msg}"); return 0
    for it in (items[:limit] if isinstance(items, list) else list(items)[:limit]):
        print(f" {fmt(it)}")
    extra = (len(items) - limit) if hasattr(items, "__len__") else 0
    if extra > 0:
        print(f" … +{extra} more")
    return len(items)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--program", default="sinjin", choices=list(PAGE_LIMIT))
    ap.add_argument("--blind", action="store_true", help="enforce 인문사회 blind-review checks")
    a = ap.parse_args()

    body = open(a.file, encoding="utf-8").read()
    issues = 0
    print(f"# 제출 전 점검: {a.file} (program={a.program})")

    # --- page budget ---
    pages, chars = estimate_pages(body)
    limit = PAGE_LIMIT[a.program]
    print(f"\n### 분량 (추정 {pages:.1f}쪽 / 본문 {chars}자, 휴리스틱)")
    if limit and pages > limit:
        print(f" 초과 추정: {pages:.1f}쪽 > 한도 {limit}쪽 — 초과분은 평가되지 않음!"); issues += 1
    elif limit:
        print(f" 한도 {limit}쪽 이내로 추정 (실제 한도는 양식 기준 확인)")
    else:
        print(" · 인문사회: 대상 사업 신청요강의 분량 기준 확인")

    # --- placeholders ---
    ph = [m.group(0) for pat in PLACEHOLDERS for m in re.finditer(pat, body)]
    issues += report("플레이스홀더 잔여", ph, "남은 [TODO]/[VERIFY]/[수치] 없음")

    # --- emoji (제안서에는 절대 금지) ---
    emo = find_emoji(body)
    issues += report("이모지(제안서 금지)", emo, "이모지 없음",
                     fmt=lambda c: f"'{c}' (U+{ord(c):04X}) 제거 필요")

    # --- hype ---
    hits = [w for w in HYPE if w in body]
    issues += report("과장·허세 표현", hits, "과장 표현 없음")

    # --- acronyms ---
    ac = find_acronyms(body)
    issues += report("약어 첫 등장 시 풀어쓰기 누락(의심)", list(ac.keys()),
                     "약어 풀어쓰기 문제 없음 (추정)",
                     fmt=lambda k: f"'{k}' — 첫 등장 시 정의 확인")

    # --- over-bold ---
    bolds = len(re.findall(r"\*\*[^*]+\*\*", body))
    print("\n### 강조 남용")
    if bolds > 25:
        print(f" **굵게** {bolds}회 — 핵심에만 사용 (전체 강조는 가독성 저하)"); issues += 1
    else:
        print(f" 강조 {bolds}회 (적정)")

    # --- citations / 참고문헌 ---
    print("\n### 참고문헌·인용")
    has_ref = bool(re.search(r"(?m)^#+\s*(참고문헌|references)", body, re.I))
    has_cite = bool(re.search(r"\[\d+\]|\(\w+\s*,?\s*\d{4}\)|doi\.org", body, re.I))
    if not has_ref: print(" 참고문헌 섹션 없음"); issues += 1
    else: print(" 참고문헌 섹션 있음")
    if not has_cite: print(" 본문 인용 표시가 보이지 않음 (모든 방법·주장 인용 권장)"); issues += 1
    else: print(" 본문 인용 표시 있음")

    # --- blind review ---
    if a.blind or a.program == "humanities":
        leaks = [m.group(0) for pat in SELF_CITE for m in re.finditer(pat, body, re.I)]
        issues += report("무기명(Blind) 신원 노출 의심", leaks,
                         "자기지칭 표현 없음 (성명·소속도 수동 점검)")

    print(f"\n{'='*48}\n총 점검 항목 경고: {issues}건. "
          "이 도구는 형식 린트이며 과학적 우수성은 Phase 5(평가 시뮬레이션)에서 판단.")
    sys.exit(1 if issues else 0)

if __name__ == "__main__":
    main()
