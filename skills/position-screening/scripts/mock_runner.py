#!/usr/bin/env python3
"""A minimal mock runner for local testing.

This runner reads stdin and emits deterministic output for the examples in
references/examples.md.

Real deployments should replace this with the real skill runtime.
"""

import sys

EX1_MARKER = "PS_EX1_STRONG_BACKEND"
EX2_MARKER = "PS_EX2_PARTIAL_EVIDENCE"
EX3_MARKER = "PS_EX3_MISALIGNED_PROFILE"
EX4_MARKER = "PS_EX4_WITH_ANSWERS"
EX5_MARKER = "PS_EX5_OVER_KEYWORDED_CV"


def run(text: str) -> str:
    s = text.strip()

    if EX1_MARKER in s:
        return (
            "Screening priorities\n"
            "Must-haves: Go in production, PostgreSQL, gRPC, Kubernetes troubleshooting\n"
            "Differentiators: Redis, mentoring, incident ownership\n"
            "Rejection risks: Thin evidence around scale, ownership depth, and incident leadership.\n"
            "\n"
            "Screening questions\n"
            "- Which Go services did the candidate own directly in production, and what changed because of their work?\n"
            "- What strong answers would prove: Direct ownership of Go services, gRPC APIs, and PostgreSQL-backed systems in production.\n"
            "- How deep is the candidate's PostgreSQL experience beyond basic usage?\n"
            "- What strong answers would prove: Depth beyond basic CRUD, including schema, query, and performance decisions in production.\n"
            "- What incidents or production failures did the candidate troubleshoot in Kubernetes?\n"
            "- What strong answers would prove: Hands-on Kubernetes troubleshooting under real production constraints.\n"
            "\n"
            "Key unresolved signal\n"
            "(standalone synthesis only; the inline `What strong answers would prove:` lines above are the one-to-one mapping)\n"
            "Concern: If scale and incident ownership stay vague, the profile may be less senior than the role expects.\n"
            "\n"
            "Preliminary fit read\n"
            "Likely fit\n"
            "\n"
            "Risks / follow-ups\n"
            "Concern: Confirm whether the candidate led incidents or mainly supported already-established systems.\n"
            "Open question: Clarify mentoring scope and whether the candidate coached other engineers directly."
        )

    if EX2_MARKER in s:
        return (
            "Screening priorities\n"
            "Must-haves: Linux production operations, Kubernetes troubleshooting, monitoring/alerting, on-call\n"
            "Differentiators: Terraform, incident leadership, service ownership\n"
            "Rejection risks: Missing direct proof of primary on-call ownership.\n"
            "\n"
            "Screening questions\n"
            "- What Linux production issues has the candidate handled directly, and how were they resolved?\n"
            "- What strong answers would prove: Verified hands-on Linux production operations rather than adjacent platform support.\n"
            "- What Kubernetes failures has the candidate debugged personally?\n"
            "- What strong answers would prove: Direct Kubernetes troubleshooting depth tied to concrete failures and recoveries.\n"
            "- What was the candidate's exact role in on-call rotations and incident response?\n"
            "- What strong answers would prove: Clear primary on-call ownership, escalation responsibility, and incident participation.\n"
            "\n"
            "Key unresolved signal\n"
            "(standalone synthesis only; the inline `What strong answers would prove:` lines above are the one-to-one mapping)\n"
            "Open question: The CV mentions platform support but does not show direct on-call ownership.\n"
            "\n"
            "Preliminary fit read\n"
            "Unclear\n"
            "\n"
            "Risks / follow-ups\n"
            "Open question: Clarify whether the candidate carried primary on-call responsibility or only assisted others.\n"
            "Concern: Terraform remains secondary; the main issue is missing proof for a core must-have."
        )

    if EX3_MARKER in s:
        return (
            "Screening priorities\n"
            "Must-haves: Modern C++, performance optimization, concurrency, Linux toolchain\n"
            "Differentiators: Systems debugging, networking, profiling depth\n"
            "Rejection risks: Missing direct evidence of modern C++, performance work, and concurrency.\n"
            "\n"
            "Screening questions\n"
            "- What direct modern C++ work has the candidate shipped recently?\n"
            "- What strong answers would prove: Credible recent hands-on C++17+ work in a production or R&D setting.\n"
            "- What performance bottlenecks has the candidate measured and improved?\n"
            "- What strong answers would prove: Real performance optimization with measurable trade-offs or profiling evidence.\n"
            "- What Linux build, debugging, or concurrency tooling has the candidate used in practice?\n"
            "- What strong answers would prove: Linux toolchain and concurrency depth rather than general software experience.\n"
            "\n"
            "Key unresolved signal\n"
            "(standalone synthesis only; the inline `What strong answers would prove:` lines above are the one-to-one mapping)\n"
            "Open question: The current CV still does not prove direct modern C++ ownership for this role.\n"
            "\n"
            "Preliminary fit read\n"
            "Likely misfit\n"
            "\n"
            "Risks / follow-ups\n"
            "Blocker: The CV does not show the core C++ and Linux toolchain experience required for this role.\n"
            "Concern: If the candidate only has adjacent frontend experience, the gap is in must-haves rather than polish."
        )

    if EX4_MARKER in s:
        return (
            "Screening priorities\n"
            "Must-haves: Python, Airflow, SQL, stakeholder ownership\n"
            "Differentiators: Pipeline reliability, cross-team communication, production ownership\n"
            "Rejection risks: Airflow ownership is claimed indirectly but not yet evidenced.\n"
            "\n"
            "Screening questions\n"
            "- What Airflow DAGs did the candidate own end to end, and what decisions did they make?\n"
            "- What strong answers would prove: Production-grade Airflow ownership rather than occasional support.\n"
            "- How did the candidate use SQL and Python together in production data workflows?\n"
            "- What strong answers would prove: Python and SQL work tied to maintained production data workflows.\n"
            "- Which stakeholders depended on the candidate's data outputs, and how was that ownership handled?\n"
            "- What strong answers would prove: Evidence of stakeholder ownership, prioritization, and communication.\n"
            "\n"
            "Key unresolved signal\n"
            "(standalone synthesis only; the inline `What strong answers would prove:` lines above are the one-to-one mapping)\n"
            "Concern: Airflow remains the key must-have because the CV signal is still weaker than the role requires.\n"
            "\n"
            "Answer analysis\n"
            "Concern: The answer suggests exposure to Airflow, but not clear end-to-end DAG ownership.\n"
            "Open question: Clarify whether the candidate designed or only supported existing Airflow pipelines.\n"
            "Concern: The CV lists Airflow, but the answer does not yet prove production ownership.\n"
            "Concern: The CV shows internal data tooling, but the answer is still weaker than the implied Airflow signal.\n"
            "\n"
            "Preliminary fit read\n"
            "Unclear\n"
            "\n"
            "Risks / follow-ups\n"
            "Open question: Ask for one concrete Airflow workflow the candidate owned, including scheduling, failures, and stakeholder impact.\n"
            "Concern: Python and SQL look plausible, but Airflow remains the key unresolved must-have."
        )

    if EX5_MARKER in s:
        return (
            "Screening priorities\n"
            "Must-haves: Kubernetes operations, Terraform, AWS, CI/CD ownership\n"
            "Differentiators: Kafka, observability, incident leadership\n"
            "Rejection risks: The CV lists many relevant tools, but the bullets do not yet prove direct ownership of the core platform work.\n"
            "\n"
            "Screening questions\n"
            "- Which Kubernetes operational tasks did the candidate own directly, and what incidents or production issues did they handle?\n"
            "- What strong answers would prove: Direct Kubernetes operations ownership rather than keyword-level familiarity.\n"
            "- What Terraform modules, infrastructure changes, or review decisions did the candidate own in AWS?\n"
            "- What strong answers would prove: Real Terraform and AWS ownership with concrete change responsibility.\n"
            "- What CI/CD pipelines did the candidate build or maintain end to end, and what changed because of their work?\n"
            "- What strong answers would prove: End-to-end CI/CD ownership instead of general deployment support.\n"
            "\n"
            "Key unresolved signal\n"
            "(standalone synthesis only; the inline `What strong answers would prove:` lines above are the one-to-one mapping)\n"
            "Concern: The resume reads keyword-rich, but the experience bullets still need proof of direct platform ownership.\n"
            "\n"
            "Preliminary fit read\n"
            "Unclear\n"
            "\n"
            "Risks / follow-ups\n"
            "Open question: Clarify whether the listed tools reflect hands-on ownership or only exposure through team environments.\n"
            "Concern: Kafka and observability strengthen the profile only after the core Kubernetes, Terraform, AWS, and CI/CD evidence is proven."
        )

    return s


if __name__ == "__main__":
    data = sys.stdin.read()
    sys.stdout.write(run(data))
