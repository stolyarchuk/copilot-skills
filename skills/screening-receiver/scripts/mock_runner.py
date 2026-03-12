#!/usr/bin/env python3
"""A minimal mock runner for local testing.

This runner reads stdin and emits deterministic output for the examples in
references/examples.md.

Real deployments should replace this with the real skill runtime.
"""

import sys

EX1_MARKER = "SR_EX1_STRONG_YES"
EX2_MARKER = "SR_EX2_BORDERLINE"
EX3_MARKER = "SR_EX3_NO_DECISION"
EX4_MARKER = "SR_EX4_CV_ANSWER_MISMATCH"
EX5_MARKER = "SR_EX5_WEAK_QUESTIONS"
EX6_MARKER = "SR_EX6_STRONG_CV_SHALLOW_OWNERSHIP"


def run(text: str) -> str:
    s = text.strip()

    if EX1_MARKER in s:
        return (
            "Question-set quality\n"
            "Must-have relevant: Production Go ownership, PostgreSQL depth, gRPC delivery, Kubernetes troubleshooting.\n"
            "Must-have relevant: production Go -> tests direct ownership of a core requirement.\n"
            "Must-have relevant: database design -> tests PostgreSQL depth for a core requirement.\n"
            "Must-have relevant: gRPC APIs -> tests direct delivery experience for a core requirement.\n"
            "Must-have relevant: Kubernetes incidents -> tests troubleshooting on a core requirement.\n"
            "\n"
            "Overall ranking\n"
            "Strong yes\n"
            "\n"
            "Evidence for fit\n"
            "- Must-have evidence: The answers show direct production ownership across Go, PostgreSQL, gRPC, and Kubernetes incidents.\n"
            "- Nice-to-have evidence: No nice-to-have signals are needed because the decision is already supported by must-have evidence.\n"
            "\n"
            "Concerns / missing proof\n"
            "- Concern: Confirm the scale of service ownership only if final-stage calibration is needed.\n"
            "\n"
            "Recommended next step\n"
            "Move to the next interview stage with this evidence set.\n"
            "\n"
            "Follow-up questions\n"
            "- Open question: Ask about service scale only if the hiring team needs level calibration."
        )

    if EX2_MARKER in s:
        return (
            "Question-set quality\n"
            "Must-have relevant: Linux incidents -> tests production troubleshooting on a core requirement.\n"
            "Must-have relevant: Kubernetes debugging -> tests a core requirement directly.\n"
            "Must-have relevant: alerting -> tests monitoring responsibility on a core requirement.\n"
            "Secondary: Terraform -> checks a nice-to-have, not the main decision driver.\n"
            "\n"
            "Overall ranking\n"
            "Borderline\n"
            "\n"
            "Evidence for fit\n"
            "- Must-have evidence: The answers support Kubernetes troubleshooting and monitoring exposure.\n"
            "- Nice-to-have evidence: Terraform is absent, but that remains secondary to the must-have on-call concern.\n"
            "\n"
            "Concerns / missing proof\n"
            "- Concern: The answers show platform support, but not enough direct on-call ownership for a core must-have.\n"
            "- Concern: Terraform is a nice-to-have gap, not the main decision driver.\n"
            "\n"
            "Recommended next step\n"
            "Run one focused follow-up on direct on-call ownership before deciding.\n"
            "\n"
            "Follow-up questions\n"
            "- Open question: What incidents did the candidate personally lead while on call?"
        )

    if EX3_MARKER in s:
        return (
            "Question-set quality\n"
            "Must-have relevant: modern C++ -> tests the core language requirement directly.\n"
            "Must-have relevant: profiling -> tests performance ownership on a core requirement.\n"
            "Must-have relevant: threading -> tests concurrency depth on a core requirement.\n"
            "\n"
            "Overall ranking\n"
            "No\n"
            "\n"
            "Evidence for fit\n"
            "- Must-have evidence: The answers remain high-level and do not establish direct ownership.\n"
            "- Nice-to-have evidence: None; the decision is blocked by missing must-have proof, not secondary gaps.\n"
            "\n"
            "Concerns / missing proof\n"
            "- Blocker: The answers do not provide credible evidence of direct modern C++ and concurrency work.\n"
            "\n"
            "Recommended next step\n"
            "Do not advance based on the current evidence.\n"
            "\n"
            "Follow-up questions\n"
            "None."
        )

    if EX4_MARKER in s:
        return (
            "Question-set quality\n"
            "Must-have relevant: Airflow DAG ownership -> tests a core requirement directly.\n"
            "Must-have relevant: SQL problem solving -> tests a core requirement directly.\n"
            "Must-have relevant: stakeholder examples -> tests a core responsibility directly.\n"
            "\n"
            "Overall ranking\n"
            "No\n"
            "\n"
            "Evidence for fit\n"
            "- Must-have evidence: The answer supports monitoring exposure, but not direct Airflow ownership.\n"
            "- Nice-to-have evidence: None; the decision is driven by missing must-have proof, not secondary gaps.\n"
            "\n"
            "Concerns / missing proof\n"
            "- Blocker: The answer contradicts the CV claim of Airflow ownership and removes confidence in a core requirement.\n"
            "- Concern: Stakeholder ownership is still unproven in the current screen.\n"
            "\n"
            "Recommended next step\n"
            "Do not advance unless the ownership contradiction is resolved with concrete evidence.\n"
            "\n"
            "Follow-up questions\n"
            "- Open question: What exact Airflow responsibilities did the candidate personally own end to end?"
        )

    if EX5_MARKER in s:
        return (
            "Question-set quality\n"
            "Weak/generic: tell me about yourself -> does not test Kubernetes, Linux, or incident response.\n"
            "Weak/generic: what are your strengths -> invites polished self-description instead of role evidence.\n"
            "Weak/generic: why this company -> tests motivation, not the technical must-haves.\n"
            "\n"
            "Overall ranking\n"
            "No\n"
            "\n"
            "Evidence for fit\n"
            "- Must-have evidence: None; the generic answers do not prove Kubernetes, Linux, or incident-response capability.\n"
            "- Nice-to-have evidence: None; the screen never reached role-specific evidence.\n"
            "\n"
            "Concerns / missing proof\n"
            "- Blocker: The original screen never tested the main technical requirements, so there is no credible evidence for the must-haves.\n"
            "\n"
            "Recommended next step\n"
            "Run a focused follow-up screen before making a decision.\n"
            "Do not advance based on this screen unless that follow-up produces credible must-have evidence.\n"
            "\n"
            "Follow-up questions\n"
            "- Open question: Ask about a real Kubernetes incident, Linux troubleshooting example, and incident-response ownership."
        )

    if EX6_MARKER in s:
        return (
            "Question-set quality\n"
            "Must-have relevant: Airflow ownership -> tests a core requirement directly.\n"
            "Must-have relevant: Spark pipeline design -> tests a core requirement directly.\n"
            "Must-have relevant: production incidents -> tests operational ownership on a core requirement.\n"
            "Must-have relevant: stakeholder decisions -> tests ownership and prioritization on a core responsibility.\n"
            "\n"
            "Overall ranking\n"
            "Borderline\n"
            "\n"
            "Evidence for fit\n"
            "- Must-have evidence: The answers show stack exposure across Airflow, Spark, SQL, and incident support, but not consistent end-to-end ownership.\n"
            "- Nice-to-have evidence: The CV suggests strong collaboration context, but the answers do not convert that into clear ownership proof.\n"
            "\n"
            "Concerns / missing proof\n"
            "- Concern: The CV reads senior, but the answers describe support work more than direct ownership of pipelines and decisions.\n"
            "- Concern: The candidate discusses incidents and stakeholder work at a high level without showing they led the critical decisions.\n"
            "\n"
            "Recommended next step\n"
            "Run one focused follow-up on direct ownership before deciding.\n"
            "\n"
            "Follow-up questions\n"
            "- Open question: Which Airflow or Spark decisions did the candidate personally make without deferring to a senior engineer?"
        )

    return s


if __name__ == "__main__":
    data = sys.stdin.read()
    sys.stdout.write(run(data))
