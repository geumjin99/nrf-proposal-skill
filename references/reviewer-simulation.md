# NRF Reviewer-Panel Simulation (심사위원 평가 시뮬레이션)

> Modeled on the `nature-reviewer` skill from
> [`nature-skills`](https://github.com/Yuan1z0825/nature-skills) (peer-review-from-the-referee-side,
> 3 reviewers + cross synthesis, grounded only in a local source basis, strict non-invention).
> Writing a paper and
> writing a proposal are close cousins — the same review discipline applies. This is the engine
> behind **Phase 5**.

## Default stance

- Simulate the **referee side**, not the author's rebuttal. The goal is to *fail the draft in
  private* so it passes in public.
- Ground every judgment in **(1) the proposal text the user supplied** + **(2) the local source
  basis** (`evaluation-criteria.md` weights, the 7 reviewer questions, `writing-playbook.md`
  rejection list). Do not import outside "NRF policy" beyond these.
- Return **exactly 3 reviewer reports + 1 cross-review synthesis** unless the user asks otherwise.
- The 3 reviewers differ **only in emphasis** — do **not** invent identities, institutions,
  specialties, or biographies:
  - **Reviewer 1 — 세부전공자 (sub-field expert):** scrutinizes novelty vs prior art, method
    correctness, whether the 창신 actually lands in the method, citation adequacy.
  - **Reviewer 2 — 유능한 외부 동료 (competent outsider):** the realistic panel default — reads
    fast, penalizes weak opening, acronym soup, unclear 필요성, figures unreadable when printed
    2-up, mismatch with the call direction.
  - **Reviewer 3 — 회의론자 (skeptic):** attacks feasibility — missing preliminary data, vague
    추진전략/연차계획, over-ambitious goals vs budget/period, hype, ethics gaps.
- Distinguish clearly: **supported / weak / not assessable from the provided material.** Never
  invent results, numbers, citations, or prior-work distinctions to fill a gap — label the gap.
- Do **not** claim a selection outcome as certain, and do not state "this will be funded."

## Axes (score per the program's real weights — see `evaluation-criteria.md`)

Default 이공 basic-research axes and weights (신진연구 shown; swap per program):

| Axis | Weight | What each reviewer checks |
|---|---|---|
| 연구의 창의성·도전성 | 50 | gap clear & real? truly novel vs cited prior work? novelty visible in the method? |
| 연구 내용·방법의 적합성 | 30 | methods specific & cited? feasible? preliminary data? budget/period appropriate? |
| 연구자의 우수성 | 10 | does the track record prove capability for **this** project? |
| 연구 성과 활용·기대효과 | 10 | 학술→산업→사회, concrete (not hype)? |

For 핵심연구 use 40/30/20/10; for 인문사회 pull the program's 평가표 and **run blind** (flag any
identity leak before scoring).

## Workflow

1. **Scope check** — confirm this is a reviewer assessment (not rebuttal drafting). State the
   assessment boundary if the draft is partial.
2. **Shared fact base** — extract: 핵심 주장(과제명·가설), visible evidence (preliminary data,
   track record), claimed 기대효과, target program + call direction, visible limitations. Label
   missing sections rather than inventing them.
3. **Score 3 reviewers** — each scores every axis on the program scale with ≤2-sentence
   justifications, then lists fatal flags from the `writing-playbook.md` rejection list.
4. **Cross-review synthesis** — consensus strengths, consensus risks, where emphasis differs,
   weighted total range, verdict band (선정권 / 경계 / 탈락권).
5. **Ranked fix list** — concrete edits ordered by **score impact**; apply the high-impact ones and
   (≤2 rounds) re-simulate, showing before→after scores so the user sees the lift.

## Output contract

```text
[심사 셋업]
- 입력 범위 / 평가 경계:
- 공유 사실 기반 (핵심 주장 / 가시적 증거 / 누락 자료):
- 대상 사업 & 배점:

[Reviewer 1 — 세부전공자 관점]
- 창의성·도전성 ( /50): 점수 + 근거 1~2문장
- 내용·방법 적합성 ( /30): 점수 + 근거
- 연구자 우수성 ( /10): 점수 + 근거
- 활용·기대효과 ( /10): 점수 + 근거
- 치명적 결함(FATAL): [rejection list 항목]
- 가중 총점 ( /100) / 추천 태도:

[Reviewer 2 — 유능한 외부 동료 관점] (동일 구조)
[Reviewer 3 — 회의론자 관점] (동일 구조)

[교차 검토 종합]
- 합의된 강점:
- 합의된 기술적 위험:
- 평가자 간 강조 차이:
- 가중 총점 범위 / 판정: {선정권 | 경계 | 탈락권}
- 강한 사례가 되기 위해 반드시 해결할 사항:

[점수 영향순 수정 목록]
1) [수정] → 예상 점수 영향 2) ...

[근거 없는/평가 불가 항목]
- [the draft does not establish X; needs evidence]
```

## Red lines (mirror nature-reviewer)

- Do not invent reviewer identities, specialties, or selection history.
- Do not invent experiments, preliminary results, citations, figure details, or prior-work
  distinctions not present in the input.
- Do not silently turn the assessment into rebuttal/ghost-writing.
- Do not present the simulation as a real NRF decision letter.
- Do not assert the proposal will be funded.

## A note on "proposals with reviewer comments"

Real NRF proposals annotated with referee comments are essentially **not public** (they contain
unpublished ideas + personal data). So this simulation is grounded in the **documented evaluation
criteria** and the reviewer-comment *patterns* surfaced in the literature (e.g. 문우경 2022 quotes
real review remarks like *"문제의식은 참신한데 참신성이 연구수행과정에 반영되지 않았다"* and
*"선행연구 기반으로 추진체계가 매우 구체적이고 적절"*). Treat those as the grounding for tone and
failure modes — not as a claim to possess confidential reviewer files.
