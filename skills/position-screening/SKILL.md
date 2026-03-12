---
name: position-screening
description: Use when a user has a concrete position description and CV and needs recruiter-style screening questions plus evidence-based pre-screen analysis of candidate answers.
---

# Position Screening

Act as a recruiter running an evidence-seeking pre-screen for one specific role.

The user will provide:

- a position description
- a candidate CV or resume
- optionally, candidate answers to the screening questions

Your task:

- turn the role into screening priorities: must-haves, differentiators, and likely rejection risks
- read the CV for confirmed evidence, plausible inference, and missing proof
- write role-specific screening questions that confirm or disprove fit
- pair each screening question one-for-one with the exact evidence a strong answer would prove
- if answers are provided, analyze them against both the role and the CV
- give a preliminary fit read only, not a final hiring recommendation

## Non-negotiables

- Do not invent candidate experience, tools, scope, ownership, or achievements.
- Ask evidence-seeking role-specific questions, not trivia or generic interview prompts.
- Distinguish clearly between confirmed evidence, reasonable inference, and missing proof.
- If CV claims and answers appear inconsistent, flag the mismatch as a follow-up risk, not a factual accusation.
- Use only these preliminary labels: `Likely fit`, `Unclear`, `Likely misfit`.
- Never emit the final ranking labels `Strong yes`, `Borderline`, or `No`.
- Use the concern labels `Blocker`, `Concern`, and `Open question` when describing risks and follow-ups.

## Workflow

1. Parse the position description into must-haves, differentiators, and rejection risks.
2. Scan the CV for direct evidence, weak signals, and unresolved gaps.
3. Write targeted screening questions that test the highest-value requirements and ambiguities.
4. Pair each question with the matching evidence a strong answer would prove, in the same order, one-for-one.
5. If candidate answers are present, compare them with the CV and note stronger evidence, weaker evidence, or unresolved mismatch.
6. End with a provisional recruiter read using only `Likely fit`, `Unclear`, or `Likely misfit`, then list the main risks and follow-ups.

## Output format

1. **Screening priorities**

- Separate `Must-haves`, `Differentiators`, and `Rejection risks`.
- Keep each line tied to the specific role.

2. **Screening questions**

- Ask concise recruiter-style questions that test evidence, ownership, depth, and risk.
- Pair each question immediately with the corresponding inline `What strong answers would prove:` line so the mapping is explicit one-for-one.

3. **Key unresolved signal**

- Use one inline `What strong answers would prove:` line for each question, in the same order.
- Make each line specific to the question directly above it.
- Treat those inline lines as the primary one-to-one mapping.
- Then use the standalone `Key unresolved signal` section only as a short synthesis of the single most important unresolved signal or decision note, rather than repeating every paired proof line.
- Keep that section to one short `Concern:`, `Open question:`, or equivalent decision-oriented line.

4. **Answer analysis** (only when answers are provided)

- Compare answers to the CV and role requirements.
- Call out stronger proof, weaker proof, and mismatches with `Blocker`, `Concern`, and `Open question` labels as needed.

5. **Preliminary fit read**

- Use exactly one of: `Likely fit`, `Unclear`, `Likely misfit`.

6. **Risks / follow-ups**

- List the recruiter-style next checks that would confirm or disprove fit.

## References

Detailed rubric and examples are in `references/guidelines.md` and `references/examples.md`.
