# Position Screening Skills Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two new recruiter-style skills, `position-screening` and `screening-receiver`, with clear non-overlapping behavior, deterministic examples, and passing validation/smoke tests.

**Architecture:** Mirror the existing `cv-adapter` skill layout for both new skills. Use examples as the RED phase, deterministic mock runners as the GREEN phase, and keep `SKILL.md` plus `references/guidelines.md` aligned to the approved design so both skills stay discoverable and testable.

**Tech Stack:** Markdown skill specs, Python smoke-test runner (`validate_examples.py`), Python marker-based mock runners, repository `quick_validate.py`.

---

## File Structure

Create these new directories and files:

- `skills/position-screening/SKILL.md`
- `skills/position-screening/references/guidelines.md`
- `skills/position-screening/references/examples.md`
- `skills/position-screening/scripts/validate_examples.py`
- `skills/position-screening/scripts/mock_runner.py`
- `skills/screening-receiver/SKILL.md`
- `skills/screening-receiver/references/guidelines.md`
- `skills/screening-receiver/references/examples.md`
- `skills/screening-receiver/scripts/validate_examples.py`
- `skills/screening-receiver/scripts/mock_runner.py`

Reference files to copy/adapt from:

- `skills/cv-adapter/SKILL.md`
- `skills/cv-adapter/references/examples.md`
- `skills/cv-adapter/references/guidelines.md`
- `skills/cv-adapter/scripts/validate_examples.py`
- `skills/cv-adapter/scripts/mock_runner.py`

## Chunk 1: `position-screening` Skill

### Task 1: Create deterministic RED tests for `position-screening`

**Files:**
- Create: `skills/position-screening/references/examples.md`
- Test: `skills/position-screening/scripts/validate_examples.py`

- [ ] **Step 1: Create the examples file before implementing the skill**

Add four examples with exact expected output sections in this order:
- `Screening priorities`
- `Screening questions`
- `Key unresolved signal`
- `Answer analysis` (only in the answer-analysis example)
- `Preliminary fit read`
- `Risks / follow-ups`

Use the exact `validate_examples.py` parse shape for every example:

```text
## Example N - <short title>

Input:

```text
<marker text and scenario>
```

Expected output:

```text
<exact deterministic output>
```
```

Use these exact scenario types:
- Example 1 marker: `PS_EX1_STRONG_BACKEND` -> `Preliminary fit read` is `Likely fit`; `Screening priorities` must separate `Must-haves`, `Differentiators`, and `Rejection risks`; include at least one `Concern`
- Example 2 marker: `PS_EX2_PARTIAL_EVIDENCE` -> `Preliminary fit read` is `Unclear`; include at least one `Open question`; show missing proof for a must-have while nice-to-have remains secondary
- Example 3 marker: `PS_EX3_MISALIGNED_PROFILE` -> `Preliminary fit read` is `Likely misfit`; include at least one `Blocker`; show a must-have mismatch explicitly in `Risks / follow-ups`
- Example 4 marker: `PS_EX4_WITH_ANSWERS` -> `Preliminary fit read` is `Unclear`; include `Answer analysis`, at least one `Concern`, at least one `Open question`, and one bullet that compares CV evidence to candidate answers

For each expected output, pin down 2-4 verbatim lines beyond headings so the runner implementation is deterministic. Example requirements:
- Example 1 must include `Must-haves`, `Differentiators`, and `Rejection risks` labels under `Screening priorities`
- Example 2 must include a line beginning `Open question:`
- Example 3 must include a line beginning `Blocker:`
- Example 4 must include a line beginning `Concern:` and one line beginning `Open question:`

Use these exact input stubs and required verbatim output lines:

- Example 1 input stub:
  - `PS_EX1_STRONG_BACKEND`
  - `JOB DESCRIPTION: Senior Backend Engineer (Go, PostgreSQL, gRPC, Kubernetes)`
  - `CV: Go microservices, PostgreSQL, gRPC APIs, Kubernetes production support`
  - Required output lines:
    - `Screening priorities`
    - `Must-haves: Go in production, PostgreSQL, gRPC, Kubernetes troubleshooting`
    - `Differentiators: Redis, mentoring, incident ownership`
    - `Preliminary fit read`
    - `Likely fit`

- Example 2 input stub:
  - `PS_EX2_PARTIAL_EVIDENCE`
  - `JOB DESCRIPTION: Site Reliability Engineer (Linux, Kubernetes, Prometheus/Grafana, on-call)`
  - `CV: Platform engineer, Kubernetes, monitoring, Python automation, no direct on-call detail`
  - Required output lines:
    - `Must-haves: Linux production operations, Kubernetes troubleshooting, monitoring/alerting, on-call`
    - `Open question: The CV mentions platform support but does not show direct on-call ownership.`
    - `Preliminary fit read`
    - `Unclear`

- Example 3 input stub:
  - `PS_EX3_MISALIGNED_PROFILE`
  - `JOB DESCRIPTION: C++ R&D Engineer (C++17+, performance optimization, concurrency, Linux toolchain)`
  - `CV: Frontend engineer, React, design systems, basic Node.js tooling`
  - Required output lines:
    - `Rejection risks: Missing direct evidence of modern C++, performance work, and concurrency.`
    - `Blocker: The CV does not show the core C++ and Linux toolchain experience required for this role.`
    - `Preliminary fit read`
    - `Likely misfit`

- Example 4 input stub:
  - `PS_EX4_WITH_ANSWERS`
  - `JOB DESCRIPTION: Data Platform Engineer (Python, Airflow, SQL, stakeholder ownership)`
  - `CV: Python, SQL, internal data tooling; Airflow listed in skills only`
  - `ANSWERS: Candidate says they used Airflow occasionally but cannot describe DAG ownership clearly`
  - Required output lines:
    - `Answer analysis`
    - `Concern: The answer suggests exposure to Airflow, but not clear end-to-end DAG ownership.`
    - `Open question: Clarify whether the candidate designed or only supported existing Airflow pipelines.`
    - `Concern: The CV lists Airflow, but the answer does not yet prove production ownership.`
    - `Preliminary fit read`
    - `Unclear`

- [ ] **Step 2: Copy the smoke-test harness from `cv-adapter`**

Copy `skills/cv-adapter/scripts/validate_examples.py` to `skills/position-screening/scripts/validate_examples.py` unchanged.

- [ ] **Step 3: Create a placeholder runner for behavior-first RED**

Create `skills/position-screening/scripts/mock_runner.py` with only:

```python
#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    sys.stdout.write(sys.stdin.read())
```

- [ ] **Step 4: Run the new smoke tests to verify RED**

Run:
```bash
python skills/position-screening/scripts/validate_examples.py --examples skills/position-screening/references/examples.md --runner "python skills/position-screening/scripts/mock_runner.py"
```

Expected: FAIL with unified diffs showing actual passthrough input does not match the expected structured output.

- [ ] **Step 5: Commit the RED test scaffold** (`Skipped: user instruction says do NOT commit.`)

```bash
git add skills/position-screening/references/examples.md skills/position-screening/scripts/validate_examples.py skills/position-screening/scripts/mock_runner.py
git commit -m "test: add position-screening examples"
```

### Task 2: Implement `position-screening` contract and references

**Files:**
- Create: `skills/position-screening/SKILL.md`
- Create: `skills/position-screening/references/guidelines.md`

- [ ] **Step 1: Write `SKILL.md` in the established repo shape**

Structure it exactly as:
1. YAML frontmatter
2. `# Position Screening`
3. role framing paragraph
4. `The user will provide`
5. `Your task`
6. `Non-negotiables`
7. `Workflow`
8. `Output format`
9. `References`

Frontmatter:
```yaml
---
name: position-screening
description: Use when a user has a concrete position description and CV and needs recruiter-style screening questions plus evidence-based pre-screen analysis of candidate answers.
---
```

Required content to include verbatim or near-verbatim from the spec:
- requires position description and CV/resume
- candidate answers optional
- asks role-specific evidence-seeking questions, not trivia
- uses only preliminary labels `Likely fit`, `Unclear`, `Likely misfit`
- never emits final `Strong yes` / `Borderline` / `No`
- uses concern labels `Blocker`, `Concern`, `Open question`
- distinguishes evidence, inference, and missing proof

- [ ] **Step 2: Write `references/guidelines.md` as the detailed rubric**

Include concise sections for:
- how to derive screening priorities from must-haves, differentiators, and rejection risks
- how to write strong screening questions
- how to map answers into `evidence`, `blocker`, `concern`, and `open question`
- when to choose `Likely fit`, `Unclear`, or `Likely misfit`
- how to flag CV/answer mismatch without accusation

- [ ] **Step 3: Validate metadata/content once the contract exists**

Run:
```bash
python .github/skills/skill-creator/scripts/quick_validate.py skills/position-screening
```

Expected: PASS.

- [ ] **Step 4: Commit the skill contract** (`Skipped: user instruction says do NOT commit.`)

```bash
git add skills/position-screening/SKILL.md skills/position-screening/references/guidelines.md
git commit -m "feat: add position-screening skill contract"
```

### Task 3: Implement the deterministic GREEN path for `position-screening`

**Files:**
- Modify: `skills/position-screening/scripts/mock_runner.py`
- Test: `skills/position-screening/references/examples.md`

- [ ] **Step 1: Create the mock runner by adapting `cv-adapter`**

Implement marker-based branching with one marker per example. Keep the structure identical to the `cv-adapter` runner:
- constants for 4 example markers
- `run(text: str) -> str`
- exact string returns matching `references/examples.md`
- passthrough fallback `return s`

Use deterministic headings and labels only:
- `Likely fit`, `Unclear`, `Likely misfit`
- `Blocker`, `Concern`, `Open question`

Implement exact branches for these markers and output constraints:
- `PS_EX1_STRONG_BACKEND`: include `Must-haves`, `Differentiators`, `Rejection risks`, and final `Likely fit`
- `PS_EX2_PARTIAL_EVIDENCE`: include `Open question:` and final `Unclear`
- `PS_EX3_MISALIGNED_PROFILE`: include `Blocker:` and final `Likely misfit`
- `PS_EX4_WITH_ANSWERS`: include `Answer analysis`, `Concern:`, `Open question:`, and a CV-vs-answer comparison line

- [ ] **Step 2: Re-run smoke tests to verify GREEN**

Run:
```bash
python skills/position-screening/scripts/validate_examples.py --examples skills/position-screening/references/examples.md --runner "python skills/position-screening/scripts/mock_runner.py"
```

Expected: `All tests passed`.

- [ ] **Step 3: Re-run skill validation**

Run:
```bash
python .github/skills/skill-creator/scripts/quick_validate.py skills/position-screening
```

Expected: PASS.

- [ ] **Step 4: Commit the mock runner** (`Skipped: user instruction says do NOT commit.`)

```bash
git add skills/position-screening/scripts/mock_runner.py
git commit -m "test: add position-screening mock runner"
```

## Chunk 2: `screening-receiver` Skill

### Task 4: Create deterministic RED tests for `screening-receiver`

**Files:**
- Create: `skills/screening-receiver/references/examples.md`
- Create: `skills/screening-receiver/scripts/validate_examples.py`

- [ ] **Step 1: Create the examples file before implementing the skill**

Add five examples with exact expected output sections in this order:
- `Question-set quality`
- `Overall ranking`
- `Evidence for fit`
- `Concerns / missing proof`
- `Recommended next step`
- `Follow-up questions`

Use the exact `validate_examples.py` parse shape for every example:

```text
## Example N - <short title>

Input:

```text
<marker text and scenario>
```

Expected output:

```text
<exact deterministic output>
```
```

Use these exact scenario types:
- Example 1 marker: `SR_EX1_STRONG_YES` -> `Overall ranking` is `Strong yes`; `Question-set quality` must include at least one `Must-have relevant`
- Example 2 marker: `SR_EX2_BORDERLINE` -> `Overall ranking` is `Borderline`; expected output must separate a must-have concern from a nice-to-have gap
- Example 3 marker: `SR_EX3_NO_DECISION` -> `Overall ranking` is `No`; include at least one `Blocker:`
- Example 4 marker: `SR_EX4_CV_ANSWER_MISMATCH` -> `Overall ranking` is `No`; include at least one `Blocker:` tied to contradiction between CV and answers
- Example 5 marker: `SR_EX5_WEAK_QUESTIONS` -> `Question-set quality` explicitly lists `Weak/generic`; recommendation lowers confidence because the original screen is weak

For each expected output, pin down 2-4 verbatim lines beyond headings so the runner implementation is deterministic. Example requirements:
- Example 1 must include `Must-have relevant:`
- Example 2 must include both `Concern:` and a nice-to-have gap line
- Example 3 must include `Blocker:`
- Example 5 must include `Weak/generic:`

Use these exact input stubs and required verbatim output lines:

- Example 1 input stub:
  - `SR_EX1_STRONG_YES`
  - `ROLE: Backend Engineer (Go, PostgreSQL, gRPC, Kubernetes)`
  - `QUESTIONS: production Go, database design, gRPC APIs, Kubernetes incidents`
  - `ANSWERS: candidate describes direct ownership in each area`
  - Required output lines:
    - `Question-set quality`
    - `Must-have relevant: Production Go ownership, PostgreSQL depth, gRPC delivery, Kubernetes troubleshooting.`
    - `Overall ranking`
    - `Strong yes`

- Example 2 input stub:
  - `SR_EX2_BORDERLINE`
  - `ROLE: SRE (Linux, Kubernetes, monitoring, on-call; Terraform nice-to-have)`
  - `QUESTIONS: Linux incidents, Kubernetes debugging, alerting, Terraform`
  - `ANSWERS: candidate shows monitoring and Kubernetes support, but shallow on on-call ownership and no Terraform`
  - Required output lines:
    - `Overall ranking`
    - `Borderline`
    - `Concern: The answers show platform support, but not enough direct on-call ownership for a core must-have.`
    - `Concern: Terraform is a nice-to-have gap, not the main decision driver.`

- Example 3 input stub:
  - `SR_EX3_NO_DECISION`
  - `ROLE: C++ R&D Engineer (C++17+, performance, concurrency)`
  - `QUESTIONS: modern C++, profiling, threading`
  - `ANSWERS: candidate stays high-level and cannot describe direct experience`
  - Required output lines:
    - `Overall ranking`
    - `No`
    - `Blocker: The answers do not provide credible evidence of direct modern C++ and concurrency work.`

- Example 4 input stub:
  - `SR_EX4_CV_ANSWER_MISMATCH`
  - `ROLE: Data Engineer (Airflow, SQL, stakeholder ownership)`
  - `CV: Airflow pipeline ownership`
  - `ANSWERS: candidate says they only monitored jobs and never owned DAG design`
  - Required output lines:
    - `Overall ranking`
    - `No`
    - `Blocker: The answer contradicts the CV claim of Airflow ownership and removes confidence in a core requirement.`

- Example 5 input stub:
  - `SR_EX5_WEAK_QUESTIONS`
  - `ROLE: Platform Engineer (Kubernetes, Linux, incident response)`
  - `QUESTIONS: tell me about yourself, what are your strengths, why this company`
  - `ANSWERS: polished but generic`
  - Required output lines:
    - `Question-set quality`
    - `Weak/generic: The original questions do not test the role's must-have technical requirements.`
    - `Recommended next step`
    - `Run a focused follow-up screen before making a decision.`

- [ ] **Step 2: Copy the smoke-test harness from `cv-adapter`**

Copy `skills/cv-adapter/scripts/validate_examples.py` to `skills/screening-receiver/scripts/validate_examples.py` unchanged.

- [ ] **Step 3: Create a placeholder runner for behavior-first RED**

Create `skills/screening-receiver/scripts/mock_runner.py` with only:

```python
#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    sys.stdout.write(sys.stdin.read())
```

- [ ] **Step 4: Run the new smoke tests to verify RED**

Run:
```bash
python skills/screening-receiver/scripts/validate_examples.py --examples skills/screening-receiver/references/examples.md --runner "python skills/screening-receiver/scripts/mock_runner.py"
```

Expected: FAIL with unified diffs showing actual passthrough input does not match the expected structured output.

- [ ] **Step 5: Commit the RED test scaffold** (`Skipped: user instruction says do NOT commit.`)

```bash
git add skills/screening-receiver/references/examples.md skills/screening-receiver/scripts/validate_examples.py skills/screening-receiver/scripts/mock_runner.py
git commit -m "test: add screening-receiver examples"
```

### Task 5: Implement `screening-receiver` contract and references

**Files:**
- Create: `skills/screening-receiver/SKILL.md`
- Create: `skills/screening-receiver/references/guidelines.md`

- [ ] **Step 1: Write `SKILL.md` in the established repo shape**

Structure it exactly as:
1. YAML frontmatter
2. `# Screening Receiver`
3. role framing paragraph
4. `The user will provide`
5. `Your task`
6. `Non-negotiables`
7. `Workflow`
8. `Output format`
9. `References`

Frontmatter:
```yaml
---
name: screening-receiver
description: Use when a user already has screening questions and candidate answers for a concrete role and needs an evidence-based recruiter ranking plus next-step recommendation.
---
```

Required content to include verbatim or near-verbatim from the spec:
- requires position description plus screening questions and candidate answers
- CV/resume optional for grounding
- reviews question-set quality first using `Must-have relevant`, `Secondary`, `Weak/generic`
- always outputs one final label: `Strong yes`, `Borderline`, or `No`
- uses concern labels `Blocker`, `Concern`, `Open question`
- says when evidence is too weak for confident recommendation

- [ ] **Step 2: Write `references/guidelines.md` as the decision rubric**

Include concise sections for:
- how to audit question-set quality
- how to weight must-haves versus nice-to-haves
- when to choose `Strong yes`, `Borderline`, or `No`
- how to use `Blocker`, `Concern`, `Open question`
- how to recommend the next step when the original screen is weak

- [ ] **Step 3: Validate metadata/content once the contract exists**

Run:
```bash
python .github/skills/skill-creator/scripts/quick_validate.py skills/screening-receiver
```

Expected: PASS.

- [ ] **Step 4: Commit the skill contract**

```bash
git add skills/screening-receiver/SKILL.md skills/screening-receiver/references/guidelines.md
git commit -m "feat: add screening-receiver skill contract"
```

### Task 6: Implement the deterministic GREEN path for `screening-receiver`

**Files:**
- Modify: `skills/screening-receiver/scripts/mock_runner.py`
- Test: `skills/screening-receiver/references/examples.md`

- [ ] **Step 1: Create the mock runner by adapting `cv-adapter`**

Implement marker-based branching with one marker per example. Keep the structure identical to the `cv-adapter` runner:
- constants for 5 example markers
- `run(text: str) -> str`
- exact string returns matching `references/examples.md`
- passthrough fallback `return s`

Use deterministic headings and labels only:
- `Strong yes`, `Borderline`, `No`
- `Blocker`, `Concern`, `Open question`
- `Must-have relevant`, `Secondary`, `Weak/generic`

Implement exact branches for these markers and output constraints:
- `SR_EX1_STRONG_YES`: include `Must-have relevant:` and final `Strong yes`
- `SR_EX2_BORDERLINE`: include one must-have concern, one nice-to-have gap, and final `Borderline`
- `SR_EX3_NO_DECISION`: include `Blocker:` and final `No`
- `SR_EX4_CV_ANSWER_MISMATCH`: include a contradiction-based `Blocker:` and final decision label
- `SR_EX5_WEAK_QUESTIONS`: include `Weak/generic:` plus a recommendation that confidence is limited by the poor original questions

- [ ] **Step 2: Re-run smoke tests to verify GREEN**

Run:
```bash
python skills/screening-receiver/scripts/validate_examples.py --examples skills/screening-receiver/references/examples.md --runner "python skills/screening-receiver/scripts/mock_runner.py"
```

Expected: `All tests passed`.

- [ ] **Step 3: Re-run skill validation**

Run:
```bash
python .github/skills/skill-creator/scripts/quick_validate.py skills/screening-receiver
```

Expected: PASS.

- [ ] **Step 4: Commit the mock runner**

```bash
git add skills/screening-receiver/scripts/mock_runner.py
git commit -m "test: add screening-receiver mock runner"
```

## Chunk 3: Cross-Skill Consistency and Verification

### Task 7: Align both skills and run final verification

**Files:**
- Verify: `skills/position-screening/SKILL.md`
- Verify: `skills/position-screening/references/guidelines.md`
- Verify: `skills/position-screening/references/examples.md`
- Verify: `skills/screening-receiver/SKILL.md`
- Verify: `skills/screening-receiver/references/guidelines.md`
- Verify: `skills/screening-receiver/references/examples.md`

- [ ] **Step 1: Cross-check boundary language between the two skills**

Verify these exact distinctions:
- `position-screening` creates questions and may analyze answers, but never emits `Strong yes` / `Borderline` / `No`
- `screening-receiver` consumes existing Q&A and always emits one of `Strong yes` / `Borderline` / `No`
- both skills prohibit invention and separate evidence from missing proof
- `position-screening` explicitly separates `Must-haves`, `Differentiators`, and `Rejection risks`
- `screening-receiver` explicitly separates must-have misses from nice-to-have gaps

- [ ] **Step 2: Run both metadata validators**

Run:
```bash
python .github/skills/skill-creator/scripts/quick_validate.py skills/position-screening && python .github/skills/skill-creator/scripts/quick_validate.py skills/screening-receiver
```

Expected: PASS for both skills.

- [ ] **Step 3: Run both smoke tests**

Run:
```bash
python skills/position-screening/scripts/validate_examples.py --examples skills/position-screening/references/examples.md --runner "python skills/position-screening/scripts/mock_runner.py" && python skills/screening-receiver/scripts/validate_examples.py --examples skills/screening-receiver/references/examples.md --runner "python skills/screening-receiver/scripts/mock_runner.py"
```

Expected: both test suites print `All tests passed`.

- [ ] **Step 4: Check working tree state**

Run:
```bash
git status --short
```

Expected: only intended files changed.

- [ ] **Step 5: Report implementation evidence**

Summarize:
- files created
- exact validation commands run
- smoke-test results
- final boundary between the two skills
