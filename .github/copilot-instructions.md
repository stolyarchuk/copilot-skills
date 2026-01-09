# Copilot / AI Agent Instructions for this Repo

Purpose: Help AI coding agents be productive here by highlighting repository structure, developer workflows, and project-specific conventions.

## Quick orientation

- This repo hosts modular "Skills" that package domain knowledge, small scripts, and examples to make AI agents reliable and deterministic.
- Each skill lives under `skills/<skill-name>/` and must include a `SKILL.md` with YAML frontmatter (`name` and `description`). Examples: `skills/humanize/`, `skills/cpp-modernize/`.
- The skill-authoring tooling lives under `.github/skills/skill-creator/scripts/` and is the canonical place for validation and packaging logic.

## Key conventions (must follow)

- SKILL frontmatter (enforced by `quick_validate.py`)

  - Required keys: `name` and `description`.
  - Allowed extras: `license`, `allowed-tools`, `metadata`.
  - `name`: hyphen-case (lowercase letters, digits, hyphens), max 64 chars; cannot start/end with `-` or contain `--`.
  - `description`: short, explicit "when to use" trigger text (no `<` or `>` characters), max 1024 chars.
  - Frontmatter must start the file and be delimited by `---` lines.

- Directory layout and file roles

  - `scripts/`: small, deterministic helpers and test runners (runnable; include shebang). Put code you expect agents to execute here.
  - `references/`: long-form docs, examples, guidelines; loaded only when the skill is triggered. For files >100 lines include a TOC.
  - `assets/`: binary or template files used in outputs (do not load into context by default).

- Progressive disclosure (why this layout exists)
  - Keep `SKILL.md` lean: only metadata and core guidance. Body is loaded only after a trigger to avoid wasting context tokens. Put large or versioned content in `references/`.

## Concrete validation & test patterns

- Skill sanity check

  - `python .github/skills/skill-creator/scripts/quick_validate.py <skill-folder>` — checks frontmatter format, allowed keys, naming rules, and lengths.

- Packaging

  - `python .github/skills/skill-creator/scripts/package_skill.py <skill-folder> [output-dir]` — validates then creates `<skill-name>.skill` (zip). The packager preserves paths relative to the skill's parent folder and prints added files as it runs.

- Smoke tests / examples

  - Examples must be in `references/examples.md` using this pattern:

    Input:

    ```text
    ...
    ```

    Expected output:

    ```text
    ...
    ```

  - Local smoke-test runner: `skills/<skill>/scripts/validate_examples.py` — run like:

    ```bash
    python skills/humanize/scripts/validate_examples.py --examples skills/humanize/references/examples.md --runner "python skills/humanize/scripts/mock_runner.py"
    ```

  - The runner expects a command that reads from stdin and writes the skill output to stdout. The validator supports `--fuzzy` to allow whitespace-insensitive comparisons.
  - Note: `scripts/mock_runner.py` are intentionally minimal local mocks — replace with the real skill runtime when available.

## Repo-specific examples & patterns

- Use `skills/humanize/SKILL.md` as a model for short, trigger-focused descriptions and `references/guidelines.md` for voice/style rules.
- Use `skills/cpp-modernize/references/guidelines.md` as the canonical example for formatting, style rules, and citation patterns (always cite cppreference for language features).

## Do / Don't (actionable)

- DO put deterministic or repeatedly executed logic into `scripts/` so agents can run them instead of re-writing code each time.
- DO place detailed schemata, API docs, or policies in `references/` and link them from `SKILL.md` (they are loaded only when needed).
- DO include concrete examples and expected outputs in `references/examples.md` to enable smoke tests.
- DON'T put environment setup, installation guides, or CI docs in `SKILL.md` (those belong in repo-level docs).
- DON'T change frontmatter keys or naming rules without updating `quick_validate.py`.

## Debugging & testing tips

- If packaging fails, run `quick_validate.py` first — it prints exact validation errors (invalid YAML, missing keys, unexpected frontmatter fields, name/description violations).
- Use the `validate_examples.py` smoke tests to verify runner compatibility and example correctness.
- When adding large reference files, include a short TOC to help agents find relevant sections without loading the whole file.

---

If any of this is unclear or you want different behavior (e.g., extra frontmatter fields or CI hooks for validation), tell me what should change and I will update this guidance.
