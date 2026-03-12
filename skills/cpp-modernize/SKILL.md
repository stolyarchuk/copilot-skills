---
name: cpp-modernize
description: "Use when modernizing, refactoring, or reviewing C++ code for safer C++23 upgrades, especially around ownership, ABI boundaries, performance-sensitive paths, or toolchain-sensitive library adoption."
---

# cpp-modernize

Give production-grade C++23 modernization guidance that favors incremental, low-risk improvements over rewrites.

## When to use

- The user asks how to modernize, refactor, or explain C++ code.
- The code involves ownership, lifetime, ABI, C interop, performance-sensitive loops, concurrency, or toolchain-sensitive feature adoption.
- The answer needs a concrete C++23 recommendation plus cppreference support.

## Contract

- Target `C++23` by default.
- Prefer incremental modernization over sweeping rewrites.
- Prioritize decisions in this order:
  1. fix safety and ownership first
  2. simplify interfaces second
  3. modernize algorithm/library usage third
  4. adopt newer expressive features last
- Every response must include relevant `cppreference.com` links.
- Every response must include either a `Code` section or an explicit `Internal-only example` or `No code change at boundary` section.

## Allowed response shapes

Use one of these exact section sets.

### Standard shape

1. `Assessment`
2. `Recommended change`
3. `Code`
4. `Why`
5. `Trade-offs`
6. `When not to do this`
7. `References`

Use this for normal modernization advice where a direct code change is appropriate.

### Compact restraint shape

1. `Assessment`
2. `Recommended change`
3. `Why`
4. `Trade-offs`
5. `Internal-only example` or `No code change at boundary`
6. `References`

Use this for short or boundary-sensitive questions when the safest answer is to preserve a boundary, keep the existing form, or modernize only internally.

## Required judgment rules

- Name at least one real production risk in `Assessment`.
- Avoid blanket modernization advice; explain what should stay stable if that is the safer choice.
- Mention compatibility, support, migration, or performance caveats whenever they materially affect the recommendation.
- Prefer standard-library solutions unless the user asks for something else.
- Keep code examples short, focused, and realistic for production code.

## Explicit restraint cases

- For ambiguous raw-pointer APIs, do not assign ownership semantics until ownership and lifetime are clarified.
- For ABI-sensitive public interfaces, plugin boundaries, shared-library APIs, or C interop, call out compatibility consequences before suggesting signature changes.
- For hot paths, allocator-sensitive code, or branch-heavy loops, do not assume ranges/views are an upgrade; account for lifetime, debug cost, and runtime overhead.
- For exception-disabled or policy-constrained codebases, do not recommend `std::expected` or other newer facilities without mentioning toolchain support and migration impact.
- For concurrency-sensitive code, preserve thread-safety and memory-order assumptions before proposing more expressive constructs.

## Forbidden weak patterns

- Replacing raw pointers with smart pointers without clarifying ownership and lifetime.
- Recommending `std::format`, coroutines, `std::expected`, or similar features without mentioning support or migration implications when relevant.
- Changing ABI-sensitive or C-facing interfaces without explicitly calling out compatibility consequences.
- Suggesting ranges/views where lifetime, debug complexity, or hot-path costs make them a poor fit.

## References

- See `references/guidelines.md` for the production decision guide.
- See `references/examples.md` for sample prompts and expected outputs.
