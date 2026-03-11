# Humanize Skill Improvement Design

Date: 2026-03-11
Skill: `skills/humanize`
Scope: Tighten prompt quality with a strict output contract and explicit enforcement rules.

## Goals

- Make `humanize` behavior consistent across inputs.
- Enforce a strict engineer-to-engineer style with no corporate or AI filler.
- Preserve technical artifacts exactly while improving clarity and concision.
- Keep factual integrity: no invention, no over-assertion, clear uncertainty handling.

## Non-Goals

- Redesigning the entire validation framework.
- Adding runtime-only enforcement outside skill instructions/examples.
- Expanding into multi-mode rewriting in this iteration.

## Chosen Approach

Approach A: Contract-first rewrite spec.

Why this approach:

- It produces the highest consistency and easiest behavior verification.
- It aligns expected outputs with explicit, testable constraints.
- It avoids ambiguous guidance that can drift over time.

## Design

### 1) Skill Contract in `SKILL.md`

`SKILL.md` becomes the canonical behavior contract using strict "must" language.

Required output contract:

1. Start with a concise 1-2 sentence summary.
2. Apply deterministic structure rules:
   - Single-point informational input -> summary only.
   - Procedural input (contains actions/sequence) -> summary + numbered steps.
   - Status/diagnostic input (incident, regression, proposal, analysis) -> summary + labeled lines.

Required preservation contract:

- Preserve these artifacts verbatim at line/block level: commands, fenced code blocks, config snippets, stack traces, logs, and exact error strings.
- Do not rewrite quoted prose unless it is part of the user-authored narrative outside preserved artifacts.
- For mixed lines, preserve the technical literal segment and rewrite only surrounding prose.

Required language contract:

- Rewrite banned corporate/AI filler every time.
- Do not pass through banned phrasing unless it appears inside preserved verbatim technical artifacts.

Required truthfulness contract:

- Do not invent facts, APIs, timelines, metrics, outcomes, or certainty.
- If input is ambiguous, keep ambiguity and state it directly.

### 2) Explicit Rewrite Procedure in `SKILL.md`

Add a fixed rewrite procedure:

1. Extract core facts and constraints from input.
2. Remove filler/marketing language while preserving meaning.
3. Rewrite into strict structured output.
4. Run final compliance checks:
   - no banned filler
   - no invented facts
   - preserved verbatim technical artifacts
   - concise wording

Formatting decision rules:

- Numbered list for procedures/step-by-step actions.
- Labeled lines (for example `Summary:`, `Impact:`, `Next steps:`) for diagnosis/status updates.

Decision examples:

- Input type: one short announcement -> output `Summary:` line only.
- Input type: migration/runbook instructions -> output `Summary:` + numbered steps.
- Input type: outage/root-cause note -> output `Summary:` + `Impact:` + `Next steps:`.

### 3) Reference and Example Alignment

Update `references/guidelines.md` to mirror the same strict contract and procedure so `SKILL.md` and reference guidance are consistent.

Fix `references/guidelines.md` frontmatter metadata to align with repository conventions and avoid conflicting tool/schema metadata.

Update `references/examples.md` expected outputs so they consistently reflect:

- summary-first structure
- strict direct language
- explicit uncertainty when needed
- preserved technical literals

### 4) Validation Strategy

Keep `scripts/validate_examples.py` implementation unchanged for this iteration.

Enforcement in this scope is example-driven only. Use stronger example expectations as the primary mechanism so failures catch behavior drift without validator logic changes.

Required additional example coverage:

- invention-risk case (input lacks metrics; expected output must not invent any)
- ambiguity case (expected output must include explicit uncertainty wording)
- artifact-boundary case (mixed prose + command/log line; literal must remain exact)

## Risks and Mitigations

- Risk: Overly rigid formatting may reduce naturalness for short inputs.
  - Mitigation: Keep structure strict but concise; avoid unnecessary labels for trivial single-line rewrites.

- Risk: Banned language list may conflict with quoted source text.
  - Mitigation: Preserve verbatim technical artifacts only; otherwise rewrite banned terms.

- Risk: Guidance duplication between `SKILL.md` and references may drift.
  - Mitigation: Treat `SKILL.md` as source of truth and keep references aligned in same change.

## Test Plan

Run skill-specific checks after implementation edits:

1. Validate metadata/content:

```bash
python .github/skills/skill-creator/scripts/quick_validate.py skills/humanize
```

2. Run humanize smoke tests:

```bash
python skills/humanize/scripts/validate_examples.py --examples skills/humanize/references/examples.md --runner "python skills/humanize/scripts/mock_runner.py"
```

## Rollout Plan

1. Update `SKILL.md` with strict contract and explicit rewrite procedure.
2. Align `references/guidelines.md` and `references/examples.md` with the contract.
3. Run validation + smoke tests.
4. Run go/no-go gates:
   - `quick_validate` passes for `skills/humanize`
   - smoke tests pass for `skills/humanize`
   - manual spot-check set (3 samples: procedural, diagnostic, mixed artifact) reviewed and accepted
5. If regression appears in structure or artifact preservation, rollback by restoring previous examples/contract edits in the same PR branch and re-apply incrementally.

## Acceptance Criteria

- `SKILL.md` includes explicit structure decision rules for single-point, procedural, and diagnostic inputs.
- `SKILL.md` includes explicit artifact-boundary preservation rules.
- Zero banned phrases appear in expected outputs outside preserved verbatim artifacts.
- References match `SKILL.md` policy without contradictions.
- Examples include at least one case each for invention-risk, ambiguity handling, and artifact-boundary preservation.
- `quick_validate` and skill smoke tests pass.
