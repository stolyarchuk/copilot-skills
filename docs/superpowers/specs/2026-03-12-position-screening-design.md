# Position Screening Skills Design

Date: 2026-03-12
Skills: `skills/position-screening`, `skills/screening-receiver`
Scope: Add two recruiter-style skills for pre-screen question design, answer analysis, and candidate ranking against a concrete position.

## Goals

- Add a `position-screening` skill that turns a job description and CV into recruiter-grade screening questions and, when answers are provided, evaluates those answers.
- Add a `screening-receiver` skill that evaluates existing screening questions and candidate answers against a role and produces a ranking-style hiring recommendation.
- Keep both skills evidence-based, recruiter-oriented, and explicitly non-fictional.
- Follow the existing repo pattern used by `cv-adapter` and `cv-improver`: concise `SKILL.md`, supporting guidance, example-driven smoke tests, and deterministic mock runners.

## Non-Goals

- Building a generalized interview framework for all interview stages.
- Producing automated numeric scoring logic outside the skill text and examples.
- Replacing `cv-adapter`; these new skills complement it.

## Chosen Approach

Approach A: split the workflow into an upstream generation-and-analysis skill plus a downstream assessment-only skill.

Why this approach:

- It keeps each skill discoverable by intent: create-and-run screening vs assess completed screening.
- It avoids muddy overlap where both skills generate questions and score answers.
- It mirrors real usage: one user may want help creating screening questions, while another already has Q&A and only wants a ranking decision.

## Design

### 1) `position-screening` Skill Contract

`position-screening` is the end-to-end recruiter pre-screen skill.

Required inputs:

- position description
- candidate CV/resume
- optionally, candidate answers to the generated questions

Core behavior:

1. Parse the role into must-haves, strong differentiators, and likely rejection risks.
2. Read the CV for direct evidence, gaps, and ambiguity.
3. Produce targeted screening questions that help confirm or disprove fit.
4. For each question, add one inline `What strong answers would prove:` line that maps one-to-one to that question.
5. Use `Key unresolved signal` as a short synthesis of the top unresolved signal after the inline mappings.
6. If candidate answers are present, analyze them against both the role and the CV.
7. Produce a provisional pre-screen read, but not the final hiring-style ranking reserved for `screening-receiver`.

Non-negotiables:

- Do not invent candidate experience, tools, scope, or achievements.
- Do not ask trivia or generic interview questions when evidence-seeking recruiter questions would work better.
- Distinguish clearly between confirmed evidence, plausible inference, and missing proof.
- If CV claims and answers appear inconsistent, flag the mismatch carefully as a follow-up risk, not as a factual accusation.

Primary output sections:

- `Screening priorities`
- `Screening questions` (with inline `What strong answers would prove:` lines paired one-to-one)
- `Key unresolved signal`
- `Answer analysis` (only when answers exist)
- `Preliminary fit read`
- `Risks / follow-ups`

### 2) `screening-receiver` Skill Contract

`screening-receiver` is the assessment-only skill for already-completed screens.

Required inputs:

- position description
- screening questions
- candidate answers
- optionally, candidate CV/resume for extra grounding

Core behavior:

1. Parse the role into must-haves, nice-to-haves, and likely failure points.
2. Review the question set itself and classify each question as `Must-have relevant`, `Secondary`, or `Weak/generic`.
3. Evaluate the candidate answers question by question.
4. Map each answer to evidence of fit, lack of fit, or unresolved ambiguity.
5. Decide whether the existing screen is sufficient for a confident recommendation.
6. Produce the final ranking-style recommendation suitable for recruiter or hiring-manager review.

Non-negotiables:

- Do not re-generate a new question set unless the user explicitly asks for follow-up questions.
- Do not over-credit polished but low-evidence answers.
- Separate must-have misses from nice-to-have gaps.
- Make the recommendation explainable: every rank or recommendation must point back to evidence in answers and optional CV context.
- If the original questions are too generic or too weak, say so explicitly and lower confidence instead of pretending the evidence is sufficient.

Primary output sections:

- `Question-set quality`
- `Overall ranking`
- `Evidence for fit`
- `Concerns / missing proof`
- `Recommended next step`
- `Follow-up questions`

### 3) Shared Content Model and Voice

Both skills should share a common recruiter-style evaluation model so their outputs feel consistent.

Shared rules:

- Prioritize must-have requirements over broad positive tone.
- Prefer concrete evidence over self-description.
- Treat lack of detail as uncertainty, not disqualification by default.
- Explain whether a concern is a hard blocker, moderate risk, or clarifying follow-up.
- Keep language concise and decision-oriented, similar to recruiter notes rather than coaching prose.

Shared output characteristics:

- short, skimmable bullets
- evidence tied to role requirements
- explicit handling of ambiguity
- no invented facts or inferred certainty

### 4) Canonical Decision Vocabulary

To keep smoke tests stable, both skills should use fixed labels rather than free-form ranking language.

Allowed decision labels:

- `Strong yes`
- `Borderline`
- `No`

Allowed preliminary labels for `position-screening`:

- `Likely fit`
- `Unclear`
- `Likely misfit`

Allowed concern labels:

- `Blocker`
- `Concern`
- `Open question`

Usage rules:

- `position-screening` must use one of `Likely fit`, `Unclear`, or `Likely misfit` in `Preliminary fit read` and must never issue the final `Strong yes` / `Borderline` / `No` recommendation.
- `screening-receiver` should always use one of the three decision labels in `Overall ranking`.
- Both skills should use the concern labels consistently inside risk and gap bullets.

### 5) Repository Layout and Supporting Files

Each new skill should mirror the existing validated structure:

- `skills/<name>/SKILL.md`
- `skills/<name>/references/guidelines.md`
- `skills/<name>/references/examples.md`
- `skills/<name>/scripts/validate_examples.py`
- `skills/<name>/scripts/mock_runner.py`

Implementation reuse guidance:

- Reuse the current smoke-test script pattern from `cv-adapter` unless a change is required by the new example format.
- Keep mock runners deterministic and marker-based so examples are stable and easy to debug.
- Keep frontmatter limited to the repository-approved keys.

### 6) `SKILL.md` Shape

To match existing repository conventions, both new skills should follow this structure:

1. YAML frontmatter with `name` and `description`
2. Title and short recruiter-role framing
3. `The user will provide`
4. `Your task`
5. `Non-negotiables`
6. `Workflow`
7. `Output format`
8. `References`

Implementation note:

- `position-screening` should mirror the concise style of `cv-adapter`.
- `screening-receiver` can be slightly more decision-oriented, but should keep the same structural headings.

### 7) Example and Smoke-Test Strategy

`position-screening` example coverage should include:

- strong candidate whose CV supports most must-haves
- partial-fit candidate where questions expose missing evidence
- misaligned candidate where screening should reveal likely rejection risk
- answer-analysis case where candidate answers strengthen or weaken the initial CV impression

`screening-receiver` example coverage should include:

- strong answers leading to `Strong yes`
- mixed answers leading to `Borderline`
- weak answers leading to `No`
- inconsistency between CV and answers that triggers a follow-up warning
- weak or generic original questions that reduce decision confidence

Expected outputs should stay deterministic and verify:

- section structure
- must-have vs nice-to-have separation
- evidence-based reasoning
- actionable follow-up guidance
- canonical decision and concern labels
- canonical preliminary labels for `position-screening`

## Risks and Mitigations

- Risk: the two skills may feel redundant.
  - Mitigation: keep `position-screening` responsible for question generation plus provisional answer analysis, and reserve the final `Strong yes` / `Borderline` / `No` decision for `screening-receiver`.

- Risk: rankings may sound overconfident.
  - Mitigation: require explicit uncertainty language when evidence is missing or weak.

- Risk: question generation may drift into generic interview prep.
  - Mitigation: require every screening question to tie back to a role requirement, CV ambiguity, or likely hiring risk.

- Risk: output may become too verbose for recruiter-style use.
  - Mitigation: structure outputs as short sections with concise bullets and only the most decision-relevant commentary.

- Risk: `screening-receiver` is a weaker name than alternatives like `screening-evaluator`.
  - Mitigation: keep the requested name for this iteration, but ensure the description and overview make its purpose explicit for discovery.

## Test Plan

Run skill-specific checks after implementation edits:

1. Validate metadata/content for each new skill:

```bash
python .github/skills/skill-creator/scripts/quick_validate.py skills/position-screening
python .github/skills/skill-creator/scripts/quick_validate.py skills/screening-receiver
```

2. Run smoke tests for each new skill:

```bash
python skills/position-screening/scripts/validate_examples.py --examples skills/position-screening/references/examples.md --runner "python skills/position-screening/scripts/mock_runner.py"
python skills/screening-receiver/scripts/validate_examples.py --examples skills/screening-receiver/references/examples.md --runner "python skills/screening-receiver/scripts/mock_runner.py"
```

## Rollout Plan

1. Add `position-screening` skill files using the established repo structure.
2. Add `screening-receiver` skill files using the established repo structure.
3. Populate examples and deterministic mock runners for both skills.
4. Run `quick_validate` for both skills.
5. Run smoke tests for both skills.
6. If examples reveal ambiguous wording or overlap between skills, tighten `SKILL.md` contracts and re-run tests.

## Acceptance Criteria

- `skills/position-screening/SKILL.md` clearly requires both a position description and CV/resume, and optionally supports candidate answers.
- `skills/screening-receiver/SKILL.md` clearly requires position description plus screening Q&A, with CV/resume optional.
- Both skills enforce no-invention rules and distinguish evidence from inference.
- `position-screening` outputs role-specific screening questions rather than generic interview prompts.
- `position-screening` stops at a provisional pre-screen read and does not duplicate the final downstream ranking behavior.
- `position-screening` uses only `Likely fit`, `Unclear`, or `Likely misfit` for `Preliminary fit read`.
- `screening-receiver` evaluates both the question-set quality and the candidate answers, then outputs one final decision label: `Strong yes`, `Borderline`, or `No`.
- Both skills include guidelines, examples, deterministic mock runners, and smoke-test scripts.
- `quick_validate` and smoke tests pass for both skills.
