#!/usr/bin/env python3
"""A minimal mock runner for local testing.

This runner reads stdin and emits deterministic outputs for the examples in
references/examples.md.

Real deployments should replace this with the real skill runtime.
"""

import sys

EX1_MARKER = "Results-driven software engineer"
EX2_MARKER = "Optimized system for high performance"
EX3_MARKER = "Please rewrite my resume the way a recruiter wants to see it."
EX4_MARKER = "Read the updated resume again as a recruiter."


def run(text: str) -> str:
    s = text.strip()

    if EX1_MARKER in s:
        return (
            "Weak/vague phrasing:\n"
            '- "Results-driven" - Generic adjective; no evidence or outcome attached.\n'
            '- "strong communication skills" - Unprovable claim as written; no signal of how it showed up (stakeholders, docs, incidents).\n'
            '- "Responsible for developing microservices" - Responsibilities, not outcomes; no scope (how many services, ownership, runtime).\n'
            '- "Worked on performance improvements" - No baseline, delta, or target metric; reads like filler.\n'
            '- "Helped the team deliver features on time" - Low ownership; no indication of what you did or what shipped.\n'
            "\n"
            "Value gaps:\n"
            "- Missing scale: traffic/QPS, latency budgets, number of services, data stores.\n"
            "- Missing impact: what improved (p95 latency, error rate, cost) and by how much.\n"
            "- Missing ownership: what you owned end-to-end vs contributed to.\n"
            "\n"
            "Invite-to-next-stage blockers:\n"
            "- I can’t tell what you delivered or how good you are.\n"
            "- The bullets read like a job description, not evidence of impact.\n"
            "\n"
            "Questions to answer:\n"
            "- What were the concrete outcomes you shipped in the last role?\n"
            "- What performance metric changed (baseline and after) and over what timeframe?\n"
            "- How many services/systems did you own and what was their scale?\n"
            "- What was your specific role in delivering features (design, implementation, ops)?"
        )

    if EX2_MARKER in s:
        return (
            "Weak/vague phrasing:\n"
            '- "Optimized system for high performance" - "High performance" is undefined; no metric or constraint.\n'
            '- "Built scalable cloud solutions" - "Scalable" is empty without scale, workload, and result.\n'
            "\n"
            "Value gaps:\n"
            "- Missing metrics: latency/throughput/cost before vs after.\n"
            "- Missing scale: users, requests, data volume, regions.\n"
            "- Missing context: which part of the system and what trade-offs.\n"
            "\n"
            "Invite-to-next-stage blockers:\n"
            "- Reads like buzzwords; no proof.\n"
            "\n"
            "Questions to answer:\n"
            "- What metric moved and by how much?\n"
            "- What scale did the system operate at?\n"
            "- What was hard about the problem (constraints)?"
        )

    if EX3_MARKER in s:
        return (
            "Rewritten resume:\n"
            "SUMMARY\n"
            "Software engineer.\n"
            "\n"
            "EXPERIENCE\n"
            "- Reduced p95 API latency 52% (250ms → 120ms) by optimizing caching and query patterns.\n"
            "- Reduced cloud spend 18% by right-sizing instances and removing unused resources.\n"
            "- Built and owned 6 microservices (Python, Go), including design, implementation, and on-call.\n"
            "\n"
            "Missing specifics to add (no invention):\n"
            "- What was the traffic/load (QPS/users) when you achieved the latency improvement?\n"
            "- What database(s) and caching layer(s) were involved?\n"
            "- What was your on-call scope (rotation size, incidents handled, SLOs/uptime expectations)?"
        )

    if EX4_MARKER in s:
        return (
            "3 strongest points (immediately visible):\n"
            "- Clear performance impact with a concrete delta (p95 latency 250ms → 120ms).\n"
            "- Cost impact with a concrete outcome (18% reduction).\n"
            "- Ownership signal: built and owned multiple services plus on-call responsibility.\n"
            "\n"
            "Most convincing role:\n"
            "- Backend/Platform Software Engineer (mid-level), because the strongest evidence is API performance, cost efficiency, and service ownership.\n"
            "\n"
            "Interview decision:\n"
            "- Yes. There are multiple quantified outcomes and clear ownership signals that justify a screen."
        )

    return s


if __name__ == "__main__":
    data = sys.stdin.read()
    sys.stdout.write(run(data))
