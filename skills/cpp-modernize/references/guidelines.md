---
name: cpp-modernize-guidelines
description: "Production decision guide for the `cpp-modernize` skill, covering ownership, ABI boundaries, error handling, performance, concurrency, and staged C++23 adoption."
---

# Guidelines

Use this file to decide when modernization is a safe default, when it needs trade-off analysis, and when the boundary should stay stable while internals improve.

## Core rules

- Prefer incremental modernization over rewrites.
- Apply the contract order from `SKILL.md`: ownership and safety first, interface simplification second, algorithm and library usage third, newer expressive features last.
- Name at least one concrete production risk before recommending a change.
- Always mention support, migration, compatibility, or performance caveats when they materially affect the advice.
- Every recommendation should reinforce one of the allowed response shapes in `SKILL.md`.

## Three-way decision model

- **Good modernization defaults** - Use when the change improves safety or clarity without changing ownership semantics, public contracts, or hot-path behavior.
  - Example: replace `(ptr, len)` read-only inputs with `std::span<const T>` in internal code where both sides already build with a C++20+ standard library.
  - Example: replace manual index loops with `std::ranges::find_if` when lifetime is obvious and profiling does not show a regression.
- **Caution cases** - Use when the change may be right, but only after trade-off analysis around ABI, toolchain support, performance, or migration cost.
  - Example: propose `std::expected` only if the codebase permits it, the standard library support is available, and the migration path from status codes is acceptable.
  - Example: propose coroutines only if runtime integration, cancellation model, debugging cost, and compiler support are already understood.
  - Example: propose views or pipelines only if temporary lifetimes, branch predictability, and debugger readability remain acceptable.
- **Keep as-is or modernize internally only** - Use when changing the visible boundary is riskier than the modernization benefit.
  - Example: keep a shared-library `const char*` boundary stable, but use `std::string_view` internally after the call boundary.
  - Example: keep a conventional hot-loop form when a ranges pipeline would add temporary objects or hide cost.

## Ownership and lifetime

- Distinguish observer from owner before changing pointer-based APIs.
- Do not replace raw pointers with `std::unique_ptr` or `std::shared_ptr` unless transfer semantics and lifetime responsibilities are explicit.
- Treat `T*`, `const T*`, references, `std::span`, and handles as different contracts: ownership, mutability, nullability, and extent must stay clear.
- Call out nullable versus non-nullable intent explicitly; use references only when null is not a valid state and lifetime is already enforced.
- Good default: convert internal read-only buffer access to `std::span<const std::byte>` when ownership stays external and size is already known.
- Caution case: changing `T*` to `T&` or `std::span<T>` on a public API can silently remove null or sentinel semantics.
- Keep-as-is/internal-only: if ownership is undocumented, preserve the boundary and recommend documenting or splitting observer and owner paths before modernizing the type.

## API and ABI boundaries

- Be explicit about ABI-sensitive contexts: shared libraries, plugins, public headers, SDKs, serialized layouts, and C interop.
- Do not recommend signature changes across those boundaries without naming the compatibility consequence.
- `std::string_view`, `std::expected`, standard-library containers, and exception behavior can all affect ABI, binary compatibility, or language-boundary expectations.
- Good default: modernize implementation details behind a stable facade.
- Caution case: swapping a public `const char*` or out-parameter API for `std::string_view` or `std::expected` may require coordinated rebuilds, versioning, or dual-entry-point rollout.
- Keep-as-is/internal-only: keep the exported signature stable and show `No code change at boundary` or an `Internal-only example` where internals use safer types.

## Exception policy and error handling

- Check whether the codebase uses exceptions, disables them, or requires status-code style APIs.
- Do not recommend `std::expected`, exception-based construction, or throwing APIs without mentioning toolchain support and migration impact when relevant.
- Treat coroutines as an opt-in architecture change, not a default cleanup step; mention support, execution model, and migration cost before recommending them.
- Good default: modernize internal helpers first, then decide whether the boundary should expose exceptions, `std::expected`, or status objects.
- Caution case: moving from `bool` plus out-parameter to `std::expected` can improve clarity, but may conflict with exception-disabled builds, older standard libraries, or C-facing callers.
- Caution case: replacing callback, polling, or thread-based flows with coroutines may affect allocation behavior, scheduler assumptions, error propagation, and observability.
- Keep-as-is/internal-only: preserve a status-code boundary and modernize internals with clearer local helpers, enums, or error objects returned only within C++-only layers.
- When exceptions are disabled, prefer explicit result channels and make the non-throwing policy visible in the recommendation.

## Allocation and hot-path performance

- Treat allocator-sensitive paths, packet processing, parsing loops, and branch-heavy transforms as production-sensitive.
- Do not assume ranges, views, `std::format`, or extra temporary objects are improvements in hot code.
- Good default: adopt safer library utilities when cost is obvious and bounded, such as `std::span` for non-owning access or `reserve` before append-heavy work.
- Caution case: a view pipeline may look cleaner but add hidden branching, iterator adaptation, lifetime pitfalls, or harder-to-profile code.
- Keep-as-is/internal-only: keep the conventional loop when it is clearer, easier to profile, or cheaper for the allocator and branch predictor.
- Mention temporary objects, view lifetimes, debug cost, and allocator behavior when they are part of the decision.

## Concurrency and synchronization safety

- Do not modernize synchronization code unless the thread-safety contract stays explicit.
- Changing atomics, condition signaling, lock scope, or container usage can alter memory-order assumptions even if the code looks cleaner.
- Good default: prefer clarity improvements that preserve the same lock, atomic, and wake-up rules.
- Caution case: replacing a hand-written state loop with higher-level constructs may hide races, change visibility guarantees, or introduce blocking behavior.
- Keep-as-is/internal-only: preserve the boundary and current synchronization model until the user can confirm invariants, contention profile, and ownership of shared state.
- When concurrency matters, say so directly in `Assessment` and avoid speculative rewrites.

## Toolchain support and staged rollout

- Target C++23 by default, but verify compiler and standard-library availability before leaning on newer library facilities.
- Mention partial rollout options when a full migration would be disruptive.
- Good default: suggest staged adoption, such as modernizing internal call sites first or adding adapter layers around old interfaces.
- Caution case: `std::expected`, `std::format`, coroutines, modules, and some ranges-heavy patterns may require newer compilers, library versions, runtime support, or deployment coordination.
- Keep-as-is/internal-only: if support is mixed, keep the public API stable and show how internals can adopt safer types behind compatibility wrappers.
- Prefer advice that supports mixed old/new code during migration rather than requiring a flag day.

## Style guidance kept on purpose

- Keep examples short, realistic, and valid C++23.
- Prefer naming and formatting that do not distract from the modernization decision.
- Use comments only when they explain a production constraint, not to narrate obvious syntax.
- If example style does not affect ownership, compatibility, performance, or rollout decisions, keep it out of the answer.

## References

- [cppreference - std::span](https://en.cppreference.com/w/cpp/container/span)
- [cppreference - std::string_view](https://en.cppreference.com/w/cpp/string/basic_string_view)
- [cppreference - std::expected](https://en.cppreference.com/w/cpp/utility/expected)
- [cppreference - coroutines](https://en.cppreference.com/w/cpp/language/coroutines)
- [cppreference - ranges](https://en.cppreference.com/w/cpp/ranges)
- [cppreference - memory model](https://en.cppreference.com/w/cpp/language/memory_model)
