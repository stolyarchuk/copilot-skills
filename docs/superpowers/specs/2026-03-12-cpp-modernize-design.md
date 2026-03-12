# cpp-modernize Skill Improvement Design

Date: 2026-03-12
Skill: `skills/cpp-modernize`
Scope: Upgrade the skill to production-grade modernization guidance with a stricter answer contract, stronger decision rules, and better scenario coverage.

## Goals

- Make `cpp-modernize` produce safer, more production-aware modernization guidance.
- Enforce a stable answer structure that is easy to validate and hard to misuse.
- Improve scenario coverage for ownership, ABI, toolchain, allocation, interop, and performance-sensitive code.
- Keep the skill focused on practical incremental modernization rather than broad rewrites.

## Non-Goals

- Building a true C++ compiler-backed verification system.
- Expanding the generic validator beyond the current example-driven harness unless clearly necessary.
- Turning the skill into a full style guide for every C++ codebase.

## Chosen Approach

Approach A: contract + depth + test harness upgrade.

Why this approach:

- It improves real answer quality, not just formatting.
- It gives the skill clear production boundaries and trade-off rules.
- It keeps maintenance reasonable by using examples and the mock runner as the main enforcement layer.

## Design

### 1) Skill Architecture

Keep the skill split into three layers:

- `skills/cpp-modernize/SKILL.md` becomes the compact contract: trigger conditions, required response structure, hard rules, and forbidden recommendation patterns.
- `skills/cpp-modernize/references/guidelines.md` becomes the production-grade decision guide: modernization priorities, safety/performance reasoning, compatibility constraints, and when not to modernize.
- `skills/cpp-modernize/references/examples.md` becomes representative scenario coverage for realistic prompts and expected outputs.

Treat the scripts as contract verification rather than semantic C++ verification. They should confirm that representative prompts produce the right shape, decisions, and caveats.

### 2) Behavior Contract in `SKILL.md`

The skill should define two allowed response shapes so the contract stays strict but usable:

Standard shape for normal modernization advice:

1. `Assessment` - identify what is risky, dated, or acceptable as-is.
2. `Recommended change` - state the concrete modernization direction.
3. `Code` - provide a short C++23 example.
4. `Why` - explain the safety, maintainability, or performance rationale.
5. `Trade-offs` - mention one or two meaningful costs.
6. `When not to do this` - call out cases where the change is inappropriate.
7. `References` - link to relevant cppreference.com pages.

Compact restraint shape for cases where the best advice is "keep the boundary" or "modernize only internally":

1. `Assessment`
2. `Recommended change`
3. `Why`
4. `Trade-offs`
5. `Internal-only example` or `No code change at boundary`
6. `References`

Contract rule: the skill must always provide either a `Code` section or an explicit `No code change at boundary` / `Internal-only example` section, so restraint cases remain testable.

Required behavioral rules:

- Prefer incremental, low-risk modernization over sweeping rewrites.
- Optimize first for correctness and ownership clarity, then interface simplification, then library/algorithm usage, then newer expressive features.
- Use C++23 by default, but mention toolchain support constraints whenever a recommendation depends on newer library/compiler support.
- Use the compact restraint shape for short or boundary-sensitive questions when a full rewrite-style answer would add noise.

Forbidden weak patterns:

- Replacing raw pointers with smart pointers without clarifying ownership and lifetime.
- Recommending `std::format`, coroutines, `std::expected`, or similar features without mentioning support or migration implications when relevant.
- Changing ABI-sensitive or C-facing interfaces without explicitly calling out compatibility consequences.
- Suggesting ranges/views in cases where lifetime, debug complexity, or hot-path costs make them a poor fit.

### 3) Production Guidance in `references/guidelines.md`

Expand the guidance to cover production-grade decision-making rather than only style notes.

Required guidance areas:

- Ownership and lifetime: observer vs owner, transfer semantics, nullable vs non-nullable handles.
- API boundaries: ABI stability, plugin interfaces, shared libraries, public headers, and C interop.
- Error handling: exceptions vs exception-disabled builds, `std::expected`, status objects, and migration compatibility.
- Performance and allocation: temporary objects, view lifetimes, allocator-sensitive code, branchy pipelines, and hot-loop trade-offs.
- Concurrency and synchronization: avoid modernization suggestions that accidentally weaken thread-safety assumptions.
- Toolchain and rollout: compiler/library availability, partial migrations, and safe staged adoption.

The document should clearly distinguish:

- good modernization defaults
- situations that require caution
- situations where the best advice is to keep the current construct or modernize only internally

### 4) Example and Smoke-Test Coverage

Upgrade `references/examples.md` so the examples test judgment, not just snippet emission.

Required additional scenario coverage:

- ambiguous pointer ownership
- ABI-stable public API modernization request
- exception-disabled codebase choosing alternatives to exception-heavy guidance
- allocator-sensitive hot path where expressiveness may cost too much
- concurrency-sensitive code where modernization could change synchronization or memory-order assumptions
- C interop boundary where internal modernization is safer than signature changes
- loop/ranges example where a conventional loop remains clearer or cheaper

Expected outputs should include explicit restraint when appropriate, such as keeping a boundary stable while modernizing internals.

Update `scripts/mock_runner.py` to return outputs matching the new contract and to include cases where the correct recommendation is partial modernization or explicit non-adoption.

Keep `scripts/validate_examples.py` mostly unchanged in this iteration so enforcement remains example-driven.

## Risks and Mitigations

- Risk: The contract becomes too rigid for small questions.
  - Mitigation: support a compact restraint shape with fewer sections while keeping explicit decision and reference requirements.

- Risk: Examples overfit the mock runner rather than actual usage.
  - Mitigation: Use scenario variety and focus expected outputs on judgment signals, not exact prose style alone.

- Risk: Production caveats make advice verbose or timid.
  - Mitigation: Require one clear recommendation first, then concise caveats only where they materially affect correctness, compatibility, or performance.

## Test Plan

Run skill-specific checks after implementation edits:

1. Validate metadata/content:

```bash
python .github/skills/skill-creator/scripts/quick_validate.py skills/cpp-modernize
```

2. Run `cpp-modernize` smoke tests:

```bash
python skills/cpp-modernize/scripts/validate_examples.py --examples skills/cpp-modernize/references/examples.md --runner "python skills/cpp-modernize/scripts/mock_runner.py"
```

3. Add RED/GREEN skill-authoring validation:

- capture baseline failures for at least five representative prompts before editing:
  - ambiguous ownership
  - ABI-sensitive interface
  - exception-disabled environment
  - allocator-sensitive hot path
  - concurrency-sensitive modernization case
- record whether the baseline answer misses any of the following pass/fail checks:
  - identifies at least one real production risk
  - avoids blanket modernization advice
  - includes a compatibility/performance caveat when relevant
  - includes cppreference support
  - uses the standard or compact response shape correctly
- update the skill minimally to address those failures
- re-run smoke tests and manually verify the same five prompts against the same checks

## Rollout Plan

1. Capture baseline behavior and failure patterns for representative production-grade prompts.
2. Tighten `SKILL.md` to define the new contract and forbidden weak patterns.
3. Expand `references/guidelines.md` with production decision rules.
4. Upgrade `references/examples.md` and `scripts/mock_runner.py` for stronger scenario coverage.
5. Run validation and smoke tests.
6. Review whether the resulting skill remains concise, discoverable, and practical.

## Acceptance Criteria

- `SKILL.md` defines a clear response structure with explicit restraint rules.
- `SKILL.md` supports both the standard shape and compact restraint shape, with explicit rules for when each applies.
- `SKILL.md` description focuses on triggering conditions instead of workflow summary.
- `references/guidelines.md` covers ownership, ABI, error handling, allocation/performance, concurrency, toolchain constraints, and the distinction between defaults, caution cases, and keep-as-is/internal-only cases.
- `references/examples.md` includes realistic scenarios where the answer is not always "modernize everything", including at least one concurrency-sensitive case.
- `scripts/mock_runner.py` reflects the stricter output contract and partial-modernization cases.
- `quick_validate` passes for `skills/cpp-modernize`.
- `validate_examples.py` passes for `skills/cpp-modernize`.
