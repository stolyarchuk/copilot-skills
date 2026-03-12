# cpp-modernize Production Upgrade Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `cpp-modernize` so it gives production-grade C++23 modernization guidance with a stricter contract, stronger judgment rules, and broader scenario coverage.

**Architecture:** Treat `skills/cpp-modernize/SKILL.md` as the canonical answer contract, expand `skills/cpp-modernize/references/guidelines.md` into the production decision guide, and enforce the behavior through stronger examples plus a matching mock runner. Follow RED/GREEN skill-authoring flow by adding representative failing scenarios before changing the runner.

**Tech Stack:** Markdown skill docs, Python smoke-test runner (`skills/cpp-modernize/scripts/validate_examples.py`), Python mock runner (`skills/cpp-modernize/scripts/mock_runner.py`), repository validator (`.github/skills/skill-creator/scripts/quick_validate.py`).

---

## Chunk 1: Baseline and Canonical Contract

### Task 1: Capture baseline failures and tighten `SKILL.md`

**Files:**
- Modify: `skills/cpp-modernize/SKILL.md`
- Reference: `docs/superpowers/specs/2026-03-12-cpp-modernize-design.md`
- Test: `skills/cpp-modernize/references/examples.md`
- Create: `/tmp/cpp-modernize-baseline-notes.md`

- [ ] **Step 1: Capture the current baseline behavior for representative prompts**

Create `/tmp/cpp-modernize-baseline-notes.md` and record one section per prompt using these exact prompt texts:

```text
Prompt A - Ambiguous ownership
Modernize this API to C++23. The code passes raw pointers around, but the caller docs do not say whether the callee owns them:

void set_buffer(Buffer* buffer);
```

```text
Prompt B - ABI-sensitive public interface
This function is part of a public shared-library API used by third parties. Can I modernize it to std::string_view and std::expected?

extern "C++" bool parse_name(const char* input, Result* out);
```

```text
Prompt C - Exception-disabled codebase
We compile with exceptions disabled. Modernize this bool + out-parameter API:

bool load_config(Config& out);
```

```text
Prompt D - Allocator-sensitive hot path
This loop runs in a packet-processing hot path. Should I rewrite it with ranges/views?

for (size_t i = 0; i < n; ++i) {
    if ((values[i] & mask) != 0) {
        out.push_back(values[i] * scale);
    }
}
```

```text
Prompt E - Concurrency-sensitive modernization
This queue is used by multiple threads. Suggest a C++23 modernization:

while (!done_) {
    if (ready_) {
        consume(item_);
        ready_ = false;
    }
}
```

For each prompt, write a short baseline answer using only the current `skills/cpp-modernize/SKILL.md`, then record PASS/FAIL against these checks:
- missing a concrete production risk
- recommends blanket modernization
- omits compatibility or performance caveat when relevant
- omits cppreference support
- lacks the intended standard or compact response shape

Use this exact checklist wording in the note:
- `production risk named`
- `no blanket modernization`
- `caveat included when relevant`
- `cppreference included`
- `response shape correct`

- [ ] **Step 2: Rewrite the frontmatter description to focus on trigger conditions only**

Update the `description` in `skills/cpp-modernize/SKILL.md` so it starts with `Use when...` and describes triggering conditions instead of summarizing the workflow. Keep the description concise and search-friendly.

- [ ] **Step 3: Replace the current lightweight rules with the canonical contract**

Update `skills/cpp-modernize/SKILL.md` to require:
- two allowed response shapes:
  - standard shape: `Assessment`, `Recommended change`, `Code`, `Why`, `Trade-offs`, `When not to do this`, `References`
  - compact restraint shape: `Assessment`, `Recommended change`, `Why`, `Trade-offs`, `Internal-only example` or `No code change at boundary`, `References`
- a hard rule that every response includes either `Code` or an explicit boundary-preserving alternative section
- prioritization order:
  - fix safety and ownership first
  - simplify interfaces second
  - modernize algorithm/library usage third
  - adopt newer expressive features last
- explicit restraint language for ABI, C interop, hot-path, and boundary-sensitive cases
- these exact forbidden weak patterns:
  - replacing raw pointers with smart pointers without clarifying ownership and lifetime
  - recommending `std::format`, coroutines, `std::expected`, or similar features without mentioning support or migration implications when relevant
  - changing ABI-sensitive or C-facing interfaces without explicitly calling out compatibility consequences
  - suggesting ranges/views where lifetime, debug complexity, or hot-path costs make them a poor fit

- [ ] **Step 4: Re-check the same five prompts against the rewritten contract**

Using the same prompts saved in `/tmp/cpp-modernize-baseline-notes.md`, write a second short answer for each prompt and mark PASS/FAIL against the same checklist. The goal is that the rewritten contract closes the baseline failures before example updates begin.

- [ ] **Step 5: Run metadata validation after the contract rewrite**

Run: `python .github/skills/skill-creator/scripts/quick_validate.py skills/cpp-modernize`
Expected: PASS validation and no frontmatter/schema errors.

- [ ] **Step 6: Commit chunk 1 changes**

```bash
git add skills/cpp-modernize/SKILL.md
git commit -m "feat: tighten cpp-modernize response contract"
```

## Chunk 2: Production Decision Guide

### Task 2: Expand `references/guidelines.md` into a production-grade modernization guide

**Files:**
- Modify: `skills/cpp-modernize/references/guidelines.md`
- Reference: `skills/cpp-modernize/SKILL.md`

- [ ] **Step 1: Remove or reduce guidance that reads like a generic style guide**

Keep only style rules that directly support the skill's examples or recommendations. Shift the document toward production decision-making rather than broad formatting advice.

- [ ] **Step 2: Add explicit production decision sections**

Add headings and concise guidance for:
- ownership and lifetime, including observer vs owner, transfer semantics, and nullable vs non-nullable handles
- API and ABI boundaries, including plugin interfaces, shared libraries, public headers, and C interop
- exception policy and error handling, including exception-disabled builds, `std::expected`, and status-object alternatives
- allocation and hot-path performance, including temporary objects, view lifetimes, branchy pipelines, and allocator-sensitive code
- concurrency and synchronization safety, including warning against modernization that changes thread-safety or memory-order assumptions
- toolchain support and staged rollout, including compiler/library availability and partial migration guidance

- [ ] **Step 3: Add a three-way decision model**

Make the guide explicitly distinguish between:
- good modernization defaults
- caution cases that need trade-off analysis
- keep-as-is or modernize-internally-only cases

Include at least one concrete example bullet under each category.
For the `keep-as-is or modernize-internally-only` category, require one example that explicitly says the boundary stays stable while internals can change.

- [ ] **Step 4: Align the guide with the contract language in `SKILL.md`**

Ensure the guidance reinforces:
- incremental modernization over rewrites
- ownership-first prioritization
- toolchain caveats for modern library features
- restraint around ABI, C interop, ranges/views, and concurrency-sensitive changes
- the four forbidden weak patterns listed in chunk 1

- [ ] **Step 5: Re-run metadata/content validation**

Run: `python .github/skills/skill-creator/scripts/quick_validate.py skills/cpp-modernize`
Expected: PASS.

- [ ] **Step 6: Commit chunk 2 changes**

```bash
git add skills/cpp-modernize/references/guidelines.md
git commit -m "docs: expand cpp-modernize production guidance"
```

## Chunk 3: Example Coverage and RED/GREEN Enforcement

### Task 3: Add representative failing scenarios, then update the mock runner minimally

**Files:**
- Modify: `skills/cpp-modernize/references/examples.md`
- Modify: `skills/cpp-modernize/scripts/mock_runner.py`
- Test: `skills/cpp-modernize/scripts/validate_examples.py`

- [ ] **Step 1: Add new expected-output scenarios before changing the runner**

Append exactly seven new examples to `skills/cpp-modernize/references/examples.md` using the existing `Input:` / `Expected output:` fenced `text` block schema already used in that file.

Add one example for each of these cases:
- ambiguous pointer ownership
- ABI-stable library interface
- exception-disabled build
- allocator-sensitive hot path
- concurrency-sensitive code
- C interop boundary
- conventional loop preferred over ranges pipeline

Each expected output must include:
- either the standard shape or compact restraint shape from `SKILL.md`
- at least one explicit production risk
- at least one meaningful trade-off or caveat
- one cppreference link

For the ABI-stable and C interop cases, require the compact restraint shape with boundary-preserving language.
For the allocator-sensitive and conventional-loop cases, allow the recommendation to keep the loop/form if that is the safer production answer.

- [ ] **Step 2: Run the smoke tests to create the RED state**

Run:
`python skills/cpp-modernize/scripts/validate_examples.py --examples skills/cpp-modernize/references/examples.md --runner "python skills/cpp-modernize/scripts/mock_runner.py"`

Expected: FAIL, with mismatches on the seven newly added examples because `mock_runner.py` does not yet emit the new contract shape for those scenarios.

- [ ] **Step 3: Update `mock_runner.py` minimally to satisfy the new examples**

Add targeted branches only for the new scenarios. Do not redesign the runner or the validator in this iteration.

Ensure outputs now reflect:
- the standard contract shape for ordinary modernization
- the compact restraint shape for boundary-preserving cases
- explicit trade-offs and cppreference links
- explicit non-adoption or internal-only modernization where appropriate

- [ ] **Step 4: Re-run smoke tests to reach GREEN**

Run:
`python skills/cpp-modernize/scripts/validate_examples.py --examples skills/cpp-modernize/references/examples.md --runner "python skills/cpp-modernize/scripts/mock_runner.py"`

Expected: `All tests passed`.

- [ ] **Step 5: Run the repository validator again**

Run: `python .github/skills/skill-creator/scripts/quick_validate.py skills/cpp-modernize`
Expected: PASS.

- [ ] **Step 6: Commit the examples and runner together as one green increment**

```bash
git add skills/cpp-modernize/references/examples.md skills/cpp-modernize/scripts/mock_runner.py
git commit -m "test: add production-grade cpp-modernize scenarios"
```

## Chunk 4: Final Verification and Handoff

### Task 4: Confirm the skill is coherent, validated, and ready for review

**Files:**
- Verify only intended files changed:
  - `skills/cpp-modernize/SKILL.md`
  - `skills/cpp-modernize/references/guidelines.md`
  - `skills/cpp-modernize/references/examples.md`
  - `skills/cpp-modernize/scripts/mock_runner.py`
  - `docs/superpowers/specs/2026-03-12-cpp-modernize-design.md`
  - `docs/superpowers/plans/2026-03-12-cpp-modernize-production-upgrade.md`

- [ ] **Step 1: Re-check the same five baseline prompt categories manually**

Using the updated skill text and the exact prompt texts saved in `/tmp/cpp-modernize-baseline-notes.md`, manually verify the same five categories against the same checks from chunk 1.

Pass criteria for each category:
- names at least one real production risk
- avoids blanket modernization advice
- includes a compatibility or performance caveat when relevant
- includes cppreference support
- uses the standard or compact response shape correctly

- [ ] **Step 2: Check working tree state**

Run: `git status --short`
Expected: only intended `cpp-modernize` files and plan/spec docs remain modified if work is not yet committed.

- [ ] **Step 3: Re-run both final verification commands**

Run:
- `python .github/skills/skill-creator/scripts/quick_validate.py skills/cpp-modernize`
- `python skills/cpp-modernize/scripts/validate_examples.py --examples skills/cpp-modernize/references/examples.md --runner "python skills/cpp-modernize/scripts/mock_runner.py"`

Expected:
- validator: PASS
- smoke tests: `All tests passed`

- [ ] **Step 4: Confirm the result is concise, discoverable, and practical**

Manually review the final `skills/cpp-modernize/SKILL.md` and confirm:
- the description is trigger-based and search-friendly
- the top-level contract is shorter than the detailed guidance file
- the skill still reads as a practical answering guide, not a generic style manual

- [ ] **Step 5: Prepare implementation summary with evidence**

Report:
- files changed
- baseline failure themes found
- commands run
- final validator result
- final smoke-test result
