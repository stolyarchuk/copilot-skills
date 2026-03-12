# Screening Receiver - Guidelines

This skill evaluates an existing screening conversation for one concrete role. It is recruiter-style review, not a question generator.

## Inputs

Expect the user to provide:

- **Position description**: the role, must-haves, and useful secondary signals
- **Screening questions**: the exact prompts or topics already used
- **Candidate answers**: the responses that need evaluation
- **Optional CV/resume**: extra grounding for evidence or contradiction checks

## Non-negotiables

- No invention: do not add experience, ownership, tools, outcomes, or scope that the answers or CV do not support.
- Audit the question set before the candidate evaluation.
- Weight must-haves more heavily than nice-to-haves.
- If the original screen is weak, lower confidence and say so directly.

## How to audit question-set quality

Start by checking whether the original questions tested the role's core requirements.

Audit each existing screening question or prompt one by one instead of giving only an aggregate summary.
An optional aggregate summary line is allowed before the per-question audit when a concise overview helps the reader.

- **Must-have relevant**: directly tests a required skill, responsibility, or failure point.
- **Secondary**: useful context, but not central to the hiring decision.
- **Weak/generic**: broad or polished-answer questions that do not prove role fit.

In the output, show the question text and its classification explicitly, for example:

- `Must-have relevant: Kubernetes debugging -> tests a core requirement directly.`
- `Secondary: Terraform -> checks a nice-to-have, not the main decision driver.`
- `Weak/generic: tell me about yourself -> does not test the role's must-haves.`

If you use an aggregate summary line, treat it as a brief overview, not a replacement for the per-question classifications.

If the question set is mostly weak/generic, do not treat polished answers as strong evidence.

## How to weight must-haves versus nice-to-haves

- A missing must-have can drive `No` or keep the result at `Borderline` even when the candidate sounds strong elsewhere.
- A nice-to-have gap should not outweigh solid must-have evidence.
- Keep the split explicit in the write-up so the decision is easy to defend.

Mirror this split directly in the output:

- `Must-have evidence`: what the answers prove for core requirements
- `Nice-to-have evidence`: what the answers prove for secondary signals, or `None` if not relevant
- `Blocker` or `Concern` bullets for must-have misses
- separate `Concern` bullets for nice-to-have gaps when they matter but are not decisive

## Decision labels

### `Strong yes`

Use when the screening questions were strong and the answers give direct evidence for the main must-haves with no major contradictions.

### `Borderline`

Use when some must-have evidence exists, but there is still meaningful missing proof, shallow ownership, or weak original screening.

Do not use `Borderline` when the screen never tested the core must-haves and therefore provides no credible must-have evidence.

### `No`

Use when the answers miss core must-haves, stay too vague on central requirements, or contradict grounding evidence in a way that removes confidence.

## Concern labels

- **Blocker**: a hard miss, contradiction, or evidence gap on a core requirement.
- **Concern**: a moderate risk, shallow answer, or nice-to-have gap that matters but is not decisive alone.
- **Open question**: a targeted unresolved point that could change the decision if answered well.

If no targeted follow-up exists, `Follow-up questions` may contain only `None.`

## Weak-screen handling

When the original screen is weak, say that confidence is limited by the question quality.

- Do not overstate certainty.
- Do not over-credit polished but generic answers.
- Recommend a focused follow-up screen that tests the missing must-haves.
- Keep follow-up questions specific to the role's evidence gaps.

## CV and answer mismatch handling

If the CV/resume and answers do not align:

- describe the mismatch as an evidence problem, not an accusation
- explain which core requirement loses support
- use `Blocker` when the contradiction removes confidence in a must-have claim
