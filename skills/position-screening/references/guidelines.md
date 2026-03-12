# Position Screening - Guidelines

This skill helps a recruiter turn a concrete role description and candidate CV into focused pre-screen questions and a provisional evidence-based read.

Core rule: stay anchored to the role's must-haves and the candidate's actual evidence.

## Inputs

Expect the user to provide:

- **Position description**: responsibilities, must-haves, differentiators, and likely rejection risks
- **CV/resume**: pasted text is best; if PDF text is inaccessible, ask for pasted text or screenshots of the key sections
- **Candidate answers**: optional, but useful when the user wants answer analysis instead of questions alone

## Derive screening priorities first

Turn the role into three buckets:

- **Must-haves**: capabilities the candidate likely needs on day one
- **Differentiators**: useful signals that strengthen the case but should not outweigh must-have misses
- **Rejection risks**: gaps or weak signals that could stop the process early

Good priorities are concrete and role-specific. Prefer `Go in production` over `backend experience`, and `Kubernetes troubleshooting` over `cloud knowledge`.

## Read the CV with evidence discipline

For each priority, classify the CV signal as:

- **Confirmed evidence**: explicit proof in the CV
- **Plausible inference**: a reasonable but still incomplete signal
- **Missing proof**: the CV does not support the requirement enough yet

Do not upgrade inference into evidence. Missing detail is uncertainty, not automatic rejection.

## Write strong screening questions

Each question should test one of these things:

- direct ownership
- production depth
- decision-making under constraints
- scope, scale, or stakeholder responsibility
- a known gap or ambiguity from the CV

Prefer questions like:

- What did you own directly?
- What changed because of your work?
- What problem did you debug, and how?
- What requirement looks strongest on paper but is still under-evidenced?

Avoid generic or trivia-style questions that do not improve the fit decision.

Pairing rule:

- Every screening question must be followed by exactly one matching inline `What strong answers would prove:` line.
- Keep the same order from top to bottom so the reader can map question -> proof without guessing.
- Do not group several questions under one shared proof line.

## Explain what strong answers would prove

For each question, add one matching inline `What strong answers would prove:` line immediately after it. Focus on:

- role-relevant evidence
- clarified ownership
- must-have confirmation
- whether a risk should stay a `Concern`, become a `Blocker`, or move into resolved evidence

Good pattern:

- `- Question text...`
- `- What strong answers would prove: ...`

Keep the standalone `Key unresolved signal` section as a short synthesis only. It should capture the main unresolved signal, key `Concern`, or top `Open question` after the one-to-one pairings above, not restate every proof line.

Think of the output in two layers:

- inline `What strong answers would prove:` lines = the one-to-one mapping for each question
- standalone `Key unresolved signal` section = one short synthesis of the top unresolved signal after those mappings

## Analyze answers with fixed labels

When answers are present, map them into recruiter-style notes:

- **Evidence**: stronger proof than the CV alone provided
- **Concern**: partial signal, weak depth, or still-vague ownership
- **Blocker**: a must-have miss or serious contradiction that materially changes the read
- **Open question**: a gap that needs one more concrete follow-up before the decision is clear

If the CV and answers do not line up, describe that as a mismatch to verify. Do not accuse the candidate of lying unless the user already established that independently.

## Choose the preliminary fit label carefully

Use only these labels:

- **Likely fit**: most must-haves are supported, remaining gaps look confirmable rather than fundamental
- **Unclear**: the profile has plausible fit, but one or more core requirements still lack proof
- **Likely misfit**: the CV and answers do not support key must-haves strongly enough for a reasonable pre-screen pass

`Likely fit` is still provisional. This skill should never output `Strong yes`, `Borderline`, or `No`.

## Common failure modes

- treating nice-to-haves as more important than a must-have gap
- asking broad interview questions instead of evidence-seeking recruiter questions
- sounding too certain when proof is weak or indirect
- failing to separate CV evidence from answer evidence
- missing a CV-versus-answer mismatch that should trigger a follow-up
