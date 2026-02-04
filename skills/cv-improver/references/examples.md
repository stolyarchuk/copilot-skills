# Examples and Tests

This file contains example prompts and expected outputs to help validate the `cv-improver` skill.

## Example 1 - Critique-only: generic summary + responsibility bullets

Input:

```text
SUMMARY
Results-driven software engineer with strong communication skills.

EXPERIENCE
- Responsible for developing microservices.
- Worked on performance improvements.
- Helped the team deliver features on time.
```

Expected output:

```text
Weak/vague phrasing:
- "Results-driven" - Generic adjective; no evidence or outcome attached.
- "strong communication skills" - Unprovable claim as written; no signal of how it showed up (stakeholders, docs, incidents).
- "Responsible for developing microservices" - Responsibilities, not outcomes; no scope (how many services, ownership, runtime).
- "Worked on performance improvements" - No baseline, delta, or target metric; reads like filler.
- "Helped the team deliver features on time" - Low ownership; no indication of what you did or what shipped.

Value gaps:
- Missing scale: traffic/QPS, latency budgets, number of services, data stores.
- Missing impact: what improved (p95 latency, error rate, cost) and by how much.
- Missing ownership: what you owned end-to-end vs contributed to.

Invite-to-next-stage blockers:
- I can’t tell what you delivered or how good you are.
- The bullets read like a job description, not evidence of impact.

Questions to answer:
- What were the concrete outcomes you shipped in the last role?
- What performance metric changed (baseline and after) and over what timeframe?
- How many services/systems did you own and what was their scale?
- What was your specific role in delivering features (design, implementation, ops)?
```

## Example 2 - Critique-only: vague scale and buzzwords

Input:

```text
- Optimized system for high performance.
- Built scalable cloud solutions.
```

Expected output:

```text
Weak/vague phrasing:
- "Optimized system for high performance" - "High performance" is undefined; no metric or constraint.
- "Built scalable cloud solutions" - "Scalable" is empty without scale, workload, and result.

Value gaps:
- Missing metrics: latency/throughput/cost before vs after.
- Missing scale: users, requests, data volume, regions.
- Missing context: which part of the system and what trade-offs.

Invite-to-next-stage blockers:
- Reads like buzzwords; no proof.

Questions to answer:
- What metric moved and by how much?
- What scale did the system operate at?
- What was hard about the problem (constraints)?
```

## Example 3 - Rewrite mode: keep facts, improve scan-ability

Input:

```text
Please rewrite my resume the way a recruiter wants to see it.
Rules: focus on results, specifics instead of generalities, each point should answer what value I bring.
Don't invent anything. Only change wording and emphasis.

SUMMARY
Software engineer.

EXPERIENCE
- Reduced p95 API latency from 250ms to 120ms by optimizing caching and query patterns.
- Cut cloud costs by 18% by right-sizing instances and removing unused resources.
- Built 6 microservices in Python and Go; owned design, implementation, and on-call.
```

Expected output:

```text
Rewritten resume:
SUMMARY
Software engineer.

EXPERIENCE
- Reduced p95 API latency 52% (250ms → 120ms) by optimizing caching and query patterns.
- Reduced cloud spend 18% by right-sizing instances and removing unused resources.
- Built and owned 6 microservices (Python, Go), including design, implementation, and on-call.

Missing specifics to add (no invention):
- What was the traffic/load (QPS/users) when you achieved the latency improvement?
- What database(s) and caching layer(s) were involved?
- What was your on-call scope (rotation size, incidents handled, SLOs/uptime expectations)?
```

## Example 4 - Recruiter review: read the updated resume again

Input:

```text
Read the updated resume again as a recruiter.
Answer:
- what are the candidate's 3 strongest points that are immediately visible
- for which role do they look most convincing
- does the resume make you want to invite them for an interview, and why

UPDATED RESUME
SUMMARY
Software engineer.

EXPERIENCE
- Reduced p95 API latency 52% (250ms → 120ms) by optimizing caching and query patterns.
- Reduced cloud spend 18% by right-sizing instances and removing unused resources.
- Built and owned 6 microservices (Python, Go), including design, implementation, and on-call.
```

Expected output:

```text
3 strongest points (immediately visible):
- Clear performance impact with a concrete delta (p95 latency 250ms → 120ms).
- Cost impact with a concrete outcome (18% reduction).
- Ownership signal: built and owned multiple services plus on-call responsibility.

Most convincing role:
- Backend/Platform Software Engineer (mid-level), because the strongest evidence is API performance, cost efficiency, and service ownership.

Interview decision:
- Yes. There are multiple quantified outcomes and clear ownership signals that justify a screen.
```

### Running the smoke tests

```bash
python scripts/validate_examples.py --examples references/examples.md --runner "python scripts/mock_runner.py"
```
