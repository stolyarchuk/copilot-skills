#!/usr/bin/env python3
"""A minimal mock runner for local testing the doca-expert skill.

This runner reads stdin and emits a short, deterministic expert-style response for a
subset of DOCA-related prompts. It's intentionally small and deterministic so
`validate_examples.py` can smoke-test examples.
"""

import sys


def run_prompt(s: str) -> str:
    s = s.strip()
    if "5-tuple" in s or "5 tuple" in s:
        return (
            "Summary: Use a DOCA Flow table for 5-tuple matches and use queue-forward actions; program rules in batches.\n\n"
            "Checklist:\n- Use flow tables for 5-tuple match\n- Batch control-plane updates\n- Use RAII wrappers for DOCA resources\n\n"
            "C++ snippet:\n\n    struct FlowTableHandle { /* create/destroy table */ };\n    FlowTableHandle table;\n    // add 5-tuple rule -> queue\n\n"
            "References:\n- DOCA Flow SDK docs: https://docs.nvidia.com/doca/sdk/doca-flow/index.html\n- DOCA Flow API (v3.2.0): https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html"
        )
    if "tail latency" in s or "high tail" in s:
        return (
            "Summary: Tail latency usually from contention or synchronous ops; use lockless handoff and batching.\n\n"
            "Checklist:\n- Profile queues and CPU\n- Use SPSC queues for handoff\n- Batch rule updates\n\n"
            "C++ snippet:\n\n    // SPSC queue (sketch)\n    template <typename T> class SpscQueue { /*...*/ };\n\n"
            "References:\n- DOCA Flow SDK docs: https://docs.nvidia.com/doca/sdk/doca-flow/index.html\n- DOCA Flow API (v3.2.0): https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html"
        )
    # Default: echo short help sentence
    return "Ask me a DOCA Flow or SmartNIC question (e.g., '5-tuple classifier', 'tail latency')."


if __name__ == "__main__":
    data = sys.stdin.read()
    out = run_prompt(data)
    sys.stdout.write(out)
