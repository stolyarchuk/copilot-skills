# Humanize Contract-First Update Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a strict, deterministic rewrite contract for `humanize` and align guidance/examples so behavior is consistent and testable.

**Architecture:** Treat `skills/humanize/SKILL.md` as the canonical contract, with `references/guidelines.md` and `references/examples.md` aligned to it. Keep validator scripts unchanged, and enforce strictness via clearer expected outputs and added edge-case examples.

**Tech Stack:** Markdown skill specs, Python smoke-test runner (`validate_examples.py`), repository `quick_validate.py`.

---

## Chunk 1: Canonical Skill Contract

### Task 1: Update `SKILL.md` with deterministic structure and compliance checks

**Files:**
- Modify: `skills/humanize/SKILL.md`
- Test: `skills/humanize/references/examples.md`

- [ ] **Step 1: Write the target contract text in `SKILL.md`**

Add/replace sections to require:
- summary-first output (1-2 sentences)
- deterministic format selection:
  - single-point informational -> summary only
  - procedural -> summary + numbered steps
  - status/diagnostic -> summary + labeled lines
- hard banned-language rewrite rules
- artifact-preservation boundaries (commands/code/logs/errors/config)
- no-invention and explicit ambiguity handling
- final compliance checklist before output

- [ ] **Step 2: Verify no conflicting legacy rules remain**

Run: `python .github/skills/skill-creator/scripts/quick_validate.py skills/humanize`
Expected: PASS validation and no metadata/frontmatter errors.

- [ ] **Step 3: Commit chunk 1 changes**

```bash
git add skills/humanize/SKILL.md
git commit -m "feat: enforce strict humanize output contract"
```

## Chunk 2: Reference Alignment

### Task 2: Align guideline reference with canonical contract

**Files:**
- Modify: `skills/humanize/references/guidelines.md`

- [ ] **Step 1: Fix frontmatter and policy alignment**

Exact edits:
- Remove non-standard frontmatter keys and keep this file as plain guidance markdown (no conflicting skill metadata schema).
- Add explicit heading `## Deterministic output selection`.
- Add explicit heading `## Artifact boundary rules`.
- Add explicit heading `## Final compliance check`.

- [ ] **Step 2: Add deterministic formatting table and artifact boundary examples**

Add concise rules/examples for:
- summary-only case
- procedural case
- diagnostic case
- mixed literal/prose preservation

- [ ] **Step 3: Validate skill metadata/content after edits**

Run: `python .github/skills/skill-creator/scripts/quick_validate.py skills/humanize`
Expected: PASS.

- [ ] **Step 4: Commit chunk 2 changes**

```bash
git add skills/humanize/references/guidelines.md
git commit -m "docs: align humanize guidelines to strict contract"
```

## Chunk 3: Example Coverage and Verification

### Task 3: Update examples for strict enforcement and edge cases

**Files:**
- Modify: `skills/humanize/references/examples.md`
- Test: `skills/humanize/scripts/validate_examples.py`
- Test: `skills/humanize/scripts/mock_runner.py`

- [ ] **Step 1: Refresh expected outputs to strict structure**

Exact edits:
- Example 1 remains diagnostic shape (`Summary`, `Repro`, `Impact`, `Suggested next steps`).
- Example 2 rewrites marketing input into factual diagnostic/labeled output with no banned terms.
- Example 3 keeps command text unchanged (verbatim preservation).
- Example 4 includes explicit uncertainty wording (`unclear` / `not sure`).

- [ ] **Step 2: Add failing contract tests first (TDD gate)**

Add new examples with expected outputs before touching the runner:
- Example 5: single-point informational input -> summary-only output.
- Example 6: invention-risk input with missing numbers -> output must not invent metrics.
- Example 7: mixed prose + command/log line -> command/log must remain exact.

Run:
`python skills/humanize/scripts/validate_examples.py --examples skills/humanize/references/examples.md --runner "python skills/humanize/scripts/mock_runner.py"`

Expected: FAIL (new examples not implemented by mock runner yet).

- [ ] **Step 3: Update mock runner minimally to satisfy new failing tests**

Update branch matching for new examples only. Do not change validator logic in this iteration.

- [ ] **Step 4: Re-run smoke tests to green**

Run:
`python skills/humanize/scripts/validate_examples.py --examples skills/humanize/references/examples.md --runner "python skills/humanize/scripts/mock_runner.py"`

Expected: `All tests passed`.

- [ ] **Step 5: Final validation gate**

Run: `python .github/skills/skill-creator/scripts/quick_validate.py skills/humanize`
Expected: PASS.

- [ ] **Step 6: Commit examples updates separately**

```bash
git add skills/humanize/references/examples.md
git commit -m "test: add strict humanize contract examples"
```

- [ ] **Step 7: Commit mock runner adaptation separately**

```bash
git add skills/humanize/scripts/mock_runner.py
git commit -m "test: update humanize mock runner for new examples"
```

## Chunk 4: Final Sanity and Handoff

### Task 4: Confirm repository state and report

**Files:**
- Verify only intended files changed.

- [ ] **Step 1: Check working tree**

Run: `git status --short`
Expected: only expected files staged/committed, no accidental edits.

- [ ] **Step 2: Provide implementation summary with test evidence**

Report exact commands run and final pass/fail outcomes.
