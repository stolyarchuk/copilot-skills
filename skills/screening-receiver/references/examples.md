# Examples and Tests

This file contains example prompts and expected outputs to help validate the `screening-receiver` skill.

## Example 1 - Strong yes from must-have evidence

Input:

```text
SR_EX1_STRONG_YES
ROLE: Backend Engineer (Go, PostgreSQL, gRPC, Kubernetes)
QUESTIONS: production Go, database design, gRPC APIs, Kubernetes incidents
ANSWERS: candidate describes direct ownership in each area
```

Expected output:

```text
Question-set quality
Must-have relevant: Production Go ownership, PostgreSQL depth, gRPC delivery, Kubernetes troubleshooting.
Must-have relevant: production Go -> tests direct ownership of a core requirement.
Must-have relevant: database design -> tests PostgreSQL depth for a core requirement.
Must-have relevant: gRPC APIs -> tests direct delivery experience for a core requirement.
Must-have relevant: Kubernetes incidents -> tests troubleshooting on a core requirement.

Overall ranking
Strong yes

Evidence for fit
- Must-have evidence: The answers show direct production ownership across Go, PostgreSQL, gRPC, and Kubernetes incidents.
- Nice-to-have evidence: No nice-to-have signals are needed because the decision is already supported by must-have evidence.

Concerns / missing proof
- Concern: Confirm the scale of service ownership only if final-stage calibration is needed.

Recommended next step
Move to the next interview stage with this evidence set.

Follow-up questions
- Open question: Ask about service scale only if the hiring team needs level calibration.
```

## Example 2 - Borderline with must-have concern and nice-to-have gap

Input:

```text
SR_EX2_BORDERLINE
ROLE: SRE (Linux, Kubernetes, monitoring, on-call; Terraform nice-to-have)
QUESTIONS: Linux incidents, Kubernetes debugging, alerting, Terraform
ANSWERS: candidate shows monitoring and Kubernetes support, but shallow on on-call ownership and no Terraform
```

Expected output:

```text
Question-set quality
Must-have relevant: Linux incidents -> tests production troubleshooting on a core requirement.
Must-have relevant: Kubernetes debugging -> tests a core requirement directly.
Must-have relevant: alerting -> tests monitoring responsibility on a core requirement.
Secondary: Terraform -> checks a nice-to-have, not the main decision driver.

Overall ranking
Borderline

Evidence for fit
- Must-have evidence: The answers support Kubernetes troubleshooting and monitoring exposure.
- Nice-to-have evidence: Terraform is absent, but that remains secondary to the must-have on-call concern.

Concerns / missing proof
- Concern: The answers show platform support, but not enough direct on-call ownership for a core must-have.
- Concern: Terraform is a nice-to-have gap, not the main decision driver.

Recommended next step
Run one focused follow-up on direct on-call ownership before deciding.

Follow-up questions
- Open question: What incidents did the candidate personally lead while on call?
```

## Example 3 - No due to lack of credible core evidence

Input:

```text
SR_EX3_NO_DECISION
ROLE: C++ R&D Engineer (C++17+, performance, concurrency)
QUESTIONS: modern C++, profiling, threading
ANSWERS: candidate stays high-level and cannot describe direct experience
```

Expected output:

```text
Question-set quality
Must-have relevant: modern C++ -> tests the core language requirement directly.
Must-have relevant: profiling -> tests performance ownership on a core requirement.
Must-have relevant: threading -> tests concurrency depth on a core requirement.

Overall ranking
No

Evidence for fit
- Must-have evidence: The answers remain high-level and do not establish direct ownership.
- Nice-to-have evidence: None; the decision is blocked by missing must-have proof, not secondary gaps.

Concerns / missing proof
- Blocker: The answers do not provide credible evidence of direct modern C++ and concurrency work.

Recommended next step
Do not advance based on the current evidence.

Follow-up questions
None.
```

## Example 4 - No from CV and answer contradiction

Input:

```text
SR_EX4_CV_ANSWER_MISMATCH
ROLE: Data Engineer (Airflow, SQL, stakeholder ownership)
QUESTIONS: Airflow DAG ownership, SQL problem solving, stakeholder examples
CV: Airflow pipeline ownership
ANSWERS: candidate says they only monitored jobs and never owned DAG design
```

Expected output:

```text
Question-set quality
Must-have relevant: Airflow DAG ownership -> tests a core requirement directly.
Must-have relevant: SQL problem solving -> tests a core requirement directly.
Must-have relevant: stakeholder examples -> tests a core responsibility directly.

Overall ranking
No

Evidence for fit
- Must-have evidence: The answer supports monitoring exposure, but not direct Airflow ownership.
- Nice-to-have evidence: None; the decision is driven by missing must-have proof, not secondary gaps.

Concerns / missing proof
- Blocker: The answer contradicts the CV claim of Airflow ownership and removes confidence in a core requirement.
- Concern: Stakeholder ownership is still unproven in the current screen.

Recommended next step
Do not advance unless the ownership contradiction is resolved with concrete evidence.

Follow-up questions
- Open question: What exact Airflow responsibilities did the candidate personally own end to end?
```

## Example 5 - Weak original questions lower confidence

Input:

```text
SR_EX5_WEAK_QUESTIONS
ROLE: Platform Engineer (Kubernetes, Linux, incident response)
QUESTIONS: tell me about yourself, what are your strengths, why this company
ANSWERS: polished but generic
```

Expected output:

```text
Question-set quality
Weak/generic: tell me about yourself -> does not test Kubernetes, Linux, or incident response.
Weak/generic: what are your strengths -> invites polished self-description instead of role evidence.
Weak/generic: why this company -> tests motivation, not the technical must-haves.

Overall ranking
No

Evidence for fit
- Must-have evidence: None; the generic answers do not prove Kubernetes, Linux, or incident-response capability.
- Nice-to-have evidence: None; the screen never reached role-specific evidence.

Concerns / missing proof
- Blocker: The original screen never tested the main technical requirements, so there is no credible evidence for the must-haves.

Recommended next step
Run a focused follow-up screen before making a decision.
Do not advance based on this screen unless that follow-up produces credible must-have evidence.

Follow-up questions
- Open question: Ask about a real Kubernetes incident, Linux troubleshooting example, and incident-response ownership.
```

## Example 6 - Strong CV but shallow ownership answers

Input:

```text
SR_EX6_STRONG_CV_SHALLOW_OWNERSHIP
ROLE: Senior Data Engineer (Airflow, Spark, SQL, pipeline ownership)
QUESTIONS: Airflow ownership, Spark pipeline design, production incidents, stakeholder decisions
CV: Led data platform migrations, owned Airflow pipelines, improved Spark workflows, partnered with analytics and product teams
ANSWERS: candidate can name the stack but says they mostly assisted senior engineers, reviewed dashboards, and supported incidents rather than owning decisions directly
```

Expected output:

```text
Question-set quality
Must-have relevant: Airflow ownership -> tests a core requirement directly.
Must-have relevant: Spark pipeline design -> tests a core requirement directly.
Must-have relevant: production incidents -> tests operational ownership on a core requirement.
Must-have relevant: stakeholder decisions -> tests ownership and prioritization on a core responsibility.

Overall ranking
Borderline

Evidence for fit
- Must-have evidence: The answers show stack exposure across Airflow, Spark, SQL, and incident support, but not consistent end-to-end ownership.
- Nice-to-have evidence: The CV suggests strong collaboration context, but the answers do not convert that into clear ownership proof.

Concerns / missing proof
- Concern: The CV reads senior, but the answers describe support work more than direct ownership of pipelines and decisions.
- Concern: The candidate discusses incidents and stakeholder work at a high level without showing they led the critical decisions.

Recommended next step
Run one focused follow-up on direct ownership before deciding.

Follow-up questions
- Open question: Which Airflow or Spark decisions did the candidate personally make without deferring to a senior engineer?
```
