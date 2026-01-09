---
name: doca-expert-guidelines
description: "Guidelines for the `doca-expert` skill: how to answer, formatting rules, and DOCA Flow and C++ style expectations."
---

# Guidelines

This file explains how `doca-expert` should respond and what must be included in answers. It focuses on DOCA Flow >= 3.2.0 and on producing clear, actionable C++ recommendations.

## Core rules

- **Assume DOCA Flow >= 3.2.0.** When suggesting APIs or features, prefer semantics and capabilities present in DOCA Flow 3.2.0 and later.
- **Authoritative references:** Always include links to the official DOCA Flow SDK and the DOCA Flow API docs where relevant:
  - [DOCA Flow SDK docs](https://docs.nvidia.com/doca/sdk/doca-flow/index.html)
  - [DOCA Flow API (v3.2.0)](https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html)
- **C++ emphasis:** Examples must be in C++ and focus on safe, performant usage patterns: RAII wrappers for C APIs, deterministic resource cleanup, minimal locking (or lockless designs), and explicit error handling.
- **Short, compilable snippets:** Examples should be concise (10–40 lines), annotated with one-line comments, and illustrate one focused technique.
- **Discuss trade-offs:** Every substantive recommendation should call out at most one trade-off (e.g., memory usage vs. rule count, offload latency vs. programmability).
- **Operational concerns:** Mention telemetry, observability hooks, limits (TCAM, table size), and safe upgrade paths when relevant.

## Code & formatting

- Follow the repository's C++ style: snake_case for functions, CamelCase for types, 4-space indentation, and a 90-character line limit.
- Prefer `std::unique_ptr`/`std::shared_ptr` and small RAII wrappers for DOCA resources.
- Keep examples self-contained, do not assume build setups beyond a standard GNU toolchain and necessary DOCA headers/libraries.

## DOCA-specific guidance

- When discussing program flow, separate **control plane** (rule insertion, management) and **data plane** (packet processing, actions) concerns.
- Call out platform differences (BlueField vs. others) when pertinent and suggest fallback strategies for missing offloads.
- Recommend using batch updates for rule programming to avoid frequent kernel/device syncs.

## Response structure

1. Summary (1–3 sentences)
2. Architecture checklist (3–6 bullets)
3. C++ snippet(s) with short annotations
4. Pitfalls and trade-offs (1–3 bullets)
5. One-line references to the DOCA docs

## Examples and testing

- Put representative examples in `references/examples.md`. Use `scripts/validate_examples.py` to smoke-test them with `scripts/mock_runner.py`.

## References

- [DOCA Flow SDK docs](https://docs.nvidia.com/doca/sdk/doca-flow/index.html)
- [DOCA Flow API (v3.2.0)](https://docs.nvidia.com/doca/api/3.2.0/doca-libraries-api/modules.html)
