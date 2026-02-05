# CV Adapter - Guidelines

This skill adapts a resume to a specific job description (JD) the way a recruiter hiring for that role evaluates candidates: fast scan, role fit first, and evidence over buzzwords.

Core goal: in 20–30 seconds, the reader should conclude: "this candidate fits this role".

## Inputs

You should expect the user to provide:

- **Job description**: responsibilities + requirements (must-have / nice-to-have)
- **Resume**: text (preferred). If it’s a PDF and you can’t extract text, request pasted text or screenshots of key sections.

## Non-negotiables

- No invention: do not add experience, employers, dates, titles, tools, certifications, or metrics that are not present.
- Prefer minimal edits: do not rewrite the whole resume if a reorder + a few targeted edits will do.
- Preserve truthfulness and chronology.

## How to adapt (practical rubric)

### 1) Convert JD into a checklist

- Extract 5–12 bullets.
- Split into:
  - **Must-have** (hard requirements)
  - **Nice-to-have** (bonus signals)
  - **Context** (domain, team size, product type, constraints)

### 2) Map resume evidence to the checklist

For each must-have requirement:

- Find direct evidence (projects, role bullets, tools, outcomes).
- If evidence exists but is buried, move it up.
- If evidence is implied but not explicit, tighten the bullet to make the match obvious.

Do not create new claims. If the resume doesn’t support a requirement, call it a gap.

### 3) Edit strategy (minimal but high leverage)

- Reorder content so role-relevant information appears first:
  - summary / headline
  - key skills
  - most relevant experience bullets
- Within a role, reorder bullets by relevance to the JD.
- Tighten wording to emphasize:
  - ownership (owned / designed / shipped / operated)
  - measurable outcomes (only if already present)
  - production scope (systems, services, users, latency, cost)
- Downplay or remove:
  - irrelevant tech lists
  - hobbies/interests (unless they strengthen the role)
  - generic adjectives without proof

### 4) Keep structure unless structure is the problem

Default: keep the resume section structure and just reorder/tighten.

Only introduce a small new section if the resume lacks an obvious place for role-critical info. If you do, keep it minimal (e.g., "KEY SKILLS" right after the summary).

## Output requirements

### Adapted resume

- Present a single, coherent updated resume.
- Do not include meta commentary inside the resume.
- Keep formatting readable and recruiter-scan friendly.

### Fit summary (end)

- **Best-met requirements**: map JD bullets to evidence (short, direct).
- **Gaps + how to close**:
  - Identify remaining gaps.
  - Suggest concrete closure paths:
    - clarify missing details in the resume (no invention)
    - add proof (links, artifacts) if the user has them
    - reposition existing evidence
    - or acquire skill/experience (course, project, cert) if genuinely missing

## Common failure modes

- Rewriting everything instead of making targeted edits.
- Adding invented metrics.
- Leaving the most relevant experience buried.
- Keeping large irrelevant skill lists high on the page.
- Not explicitly mapping requirements to evidence at the end.
