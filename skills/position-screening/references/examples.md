# Examples and Tests

This file contains example prompts and expected outputs to help validate the `position-screening` skill.

## Example 1 - Strong backend fit

Input:

```text
PS_EX1_STRONG_BACKEND
I am screening a candidate for the Northstar Ledger backend team.
Please review this Senior Backend Engineer role and the candidate CV, then draft recruiter-style screening questions and a preliminary read.

JOB DESCRIPTION
Senior Backend Engineer working on the Northstar Ledger platform.
Must-have: Go in production, PostgreSQL, gRPC, Kubernetes troubleshooting.
Nice-to-have: Redis, mentoring, incident ownership.

CANDIDATE CV
- Backend engineer building Go microservices for B2B payments.
- Worked with PostgreSQL and gRPC APIs in production.
- Supported Kubernetes deployments and live troubleshooting.
```

Expected output:

```text
Screening priorities
Must-haves: Go in production, PostgreSQL, gRPC, Kubernetes troubleshooting
Differentiators: Redis, mentoring, incident ownership
Rejection risks: Thin evidence around scale, ownership depth, and incident leadership.

Screening questions
- Which Go services did the candidate own directly in production, and what changed because of their work?
- What strong answers would prove: Direct ownership of Go services, gRPC APIs, and PostgreSQL-backed systems in production.
- How deep is the candidate's PostgreSQL experience beyond basic usage?
- What strong answers would prove: Depth beyond basic CRUD, including schema, query, and performance decisions in production.
- What incidents or production failures did the candidate troubleshoot in Kubernetes?
- What strong answers would prove: Hands-on Kubernetes troubleshooting under real production constraints.

Key unresolved signal
(standalone synthesis only; the inline `What strong answers would prove:` lines above are the one-to-one mapping)
Concern: If scale and incident ownership stay vague, the profile may be less senior than the role expects.

Preliminary fit read
Likely fit

Risks / follow-ups
Concern: Confirm whether the candidate led incidents or mainly supported already-established systems.
Open question: Clarify mentoring scope and whether the candidate coached other engineers directly.
```

## Example 2 - Partial evidence for SRE role

Input:

```text
PS_EX2_PARTIAL_EVIDENCE
I need a pre-screen for the Harbor Cloud reliability team.
Use the role and CV below to write focused screening questions and a provisional recruiter read.

JOB DESCRIPTION
Site Reliability Engineer for Harbor Cloud.
Must-have: Linux production operations, Kubernetes troubleshooting, monitoring/alerting, on-call.
Nice-to-have: Terraform, incident leadership, service ownership.

CANDIDATE CV
- Platform engineer supporting Kubernetes clusters and monitoring.
- Built Python automation for operational tasks.
- Resume does not show direct primary on-call ownership.
```

Expected output:

```text
Screening priorities
Must-haves: Linux production operations, Kubernetes troubleshooting, monitoring/alerting, on-call
Differentiators: Terraform, incident leadership, service ownership
Rejection risks: Missing direct proof of primary on-call ownership.

Screening questions
- What Linux production issues has the candidate handled directly, and how were they resolved?
- What strong answers would prove: Verified hands-on Linux production operations rather than adjacent platform support.
- What Kubernetes failures has the candidate debugged personally?
- What strong answers would prove: Direct Kubernetes troubleshooting depth tied to concrete failures and recoveries.
- What was the candidate's exact role in on-call rotations and incident response?
- What strong answers would prove: Clear primary on-call ownership, escalation responsibility, and incident participation.

Key unresolved signal
(standalone synthesis only; the inline `What strong answers would prove:` lines above are the one-to-one mapping)
Open question: The CV mentions platform support but does not show direct on-call ownership.

Preliminary fit read
Unclear

Risks / follow-ups
Open question: Clarify whether the candidate carried primary on-call responsibility or only assisted others.
Concern: Terraform remains secondary; the main issue is missing proof for a core must-have.
```

## Example 3 - Misaligned profile

Input:

```text
PS_EX3_MISALIGNED_PROFILE
Please screen this profile for the Vector Forge systems role.
I want recruiter-style questions plus a preliminary fit read.

JOB DESCRIPTION
C++ R&D Engineer for the Vector Forge runtime team.
Must-have: modern C++, performance optimization, concurrency, Linux toolchain.
Nice-to-have: systems debugging, networking, profiling depth.

CANDIDATE CV
- Frontend engineer focused on React and design systems.
- Uses basic Node.js tooling for internal web projects.
- No direct C++ or Linux systems experience shown.
```

Expected output:

```text
Screening priorities
Must-haves: Modern C++, performance optimization, concurrency, Linux toolchain
Differentiators: Systems debugging, networking, profiling depth
Rejection risks: Missing direct evidence of modern C++, performance work, and concurrency.

Screening questions
- What direct modern C++ work has the candidate shipped recently?
- What strong answers would prove: Credible recent hands-on C++17+ work in a production or R&D setting.
- What performance bottlenecks has the candidate measured and improved?
- What strong answers would prove: Real performance optimization with measurable trade-offs or profiling evidence.
- What Linux build, debugging, or concurrency tooling has the candidate used in practice?
- What strong answers would prove: Linux toolchain and concurrency depth rather than general software experience.

Key unresolved signal
(standalone synthesis only; the inline `What strong answers would prove:` lines above are the one-to-one mapping)
Open question: The current CV still does not prove direct modern C++ ownership for this role.

Preliminary fit read
Likely misfit

Risks / follow-ups
Blocker: The CV does not show the core C++ and Linux toolchain experience required for this role.
Concern: If the candidate only has adjacent frontend experience, the gap is in must-haves rather than polish.
```

## Example 4 - Answers introduce ambiguity

Input:

```text
PS_EX4_WITH_ANSWERS
I am screening a candidate for the Meridian Metrics data platform group.
Use the role, CV, and candidate answers to produce screening questions, answer analysis, and a provisional read.

JOB DESCRIPTION
Data Platform Engineer for Meridian Metrics.
Must-have: Python, Airflow, SQL, stakeholder ownership.
Nice-to-have: pipeline reliability, cross-team communication, production ownership.

CANDIDATE CV
- Built internal data tooling with Python and SQL.
- Airflow is listed in skills, but not described in role bullets.

CANDIDATE ANSWERS
- Says they used Airflow occasionally.
- Cannot clearly describe owning DAG design end to end.
```

Expected output:

```text
Screening priorities
Must-haves: Python, Airflow, SQL, stakeholder ownership
Differentiators: Pipeline reliability, cross-team communication, production ownership
Rejection risks: Airflow ownership is claimed indirectly but not yet evidenced.

Screening questions
- What Airflow DAGs did the candidate own end to end, and what decisions did they make?
- What strong answers would prove: Production-grade Airflow ownership rather than occasional support.
- How did the candidate use SQL and Python together in production data workflows?
- What strong answers would prove: Python and SQL work tied to maintained production data workflows.
- Which stakeholders depended on the candidate's data outputs, and how was that ownership handled?
- What strong answers would prove: Evidence of stakeholder ownership, prioritization, and communication.

Key unresolved signal
(standalone synthesis only; the inline `What strong answers would prove:` lines above are the one-to-one mapping)
Concern: Airflow remains the key must-have because the CV signal is still weaker than the role requires.

Answer analysis
Concern: The answer suggests exposure to Airflow, but not clear end-to-end DAG ownership.
Open question: Clarify whether the candidate designed or only supported existing Airflow pipelines.
Concern: The CV lists Airflow, but the answer does not yet prove production ownership.
Concern: The CV shows internal data tooling, but the answer is still weaker than the implied Airflow signal.

Preliminary fit read
Unclear

Risks / follow-ups
Open question: Ask for one concrete Airflow workflow the candidate owned, including scheduling, failures, and stakeholder impact.
Concern: Python and SQL look plausible, but Airflow remains the key unresolved must-have.
```

## Example 5 - Over-keyworded CV needs proof

Input:

```text
PS_EX5_OVER_KEYWORDED_CV
I need a recruiter-style pre-screen for the Atlas Stream platform team.
Use the role and CV below to write focused screening questions and a provisional read.

JOB DESCRIPTION
Platform Engineer for Atlas Stream.
Must-have: Kubernetes operations, Terraform, AWS, CI/CD ownership.
Nice-to-have: Kafka, observability, incident leadership.

CANDIDATE CV
- Skills: Kubernetes, Terraform, AWS, Kafka, Prometheus, Grafana, Docker, GitHub Actions.
- Worked on cloud infrastructure projects.
- Helped with deployments and monitoring.
- Supported platform improvements across teams.
```

Expected output:

```text
Screening priorities
Must-haves: Kubernetes operations, Terraform, AWS, CI/CD ownership
Differentiators: Kafka, observability, incident leadership
Rejection risks: The CV lists many relevant tools, but the bullets do not yet prove direct ownership of the core platform work.

Screening questions
- Which Kubernetes operational tasks did the candidate own directly, and what incidents or production issues did they handle?
- What strong answers would prove: Direct Kubernetes operations ownership rather than keyword-level familiarity.
- What Terraform modules, infrastructure changes, or review decisions did the candidate own in AWS?
- What strong answers would prove: Real Terraform and AWS ownership with concrete change responsibility.
- What CI/CD pipelines did the candidate build or maintain end to end, and what changed because of their work?
- What strong answers would prove: End-to-end CI/CD ownership instead of general deployment support.

Key unresolved signal
(standalone synthesis only; the inline `What strong answers would prove:` lines above are the one-to-one mapping)
Concern: The resume reads keyword-rich, but the experience bullets still need proof of direct platform ownership.

Preliminary fit read
Unclear

Risks / follow-ups
Open question: Clarify whether the listed tools reflect hands-on ownership or only exposure through team environments.
Concern: Kafka and observability strengthen the profile only after the core Kubernetes, Terraform, AWS, and CI/CD evidence is proven.
```
