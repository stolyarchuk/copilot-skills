# AGENTS.md

Guidance for agentic coding assistants working in `copilot-skills`.

## What This Repo Is

- A Python-based repository for authoring and packaging modular AI skills.
- No monolithic app build exists; quality is enforced through validators + smoke tests.
- Primary structure:
  - `skills/<name>/SKILL.md` (required)
  - `skills/<name>/references/` (optional)
  - `skills/<name>/scripts/` (optional)
  - `skills/<name>/assets/` (optional)

## Source of Truth

- CI workflows:
  - `.github/workflows/skill-validation.yml`
  - `.github/workflows/package-skills.yml`
- Core tooling scripts:
  - `.github/skills/skill-creator/scripts/init_skill.py`
  - `.github/skills/skill-creator/scripts/quick_validate.py`
  - `.github/skills/skill-creator/scripts/package_skill.py`
- Copilot rules:
  - `.github/copilot-instructions.md`

## Shared Contributor Workflows

- Use `README.md` as the canonical source for setup, environment, validation, smoke-test, and packaging commands.
- There is no dedicated linter config or pytest suite in this repo; `quick_validate.py` plus example smoke tests are the quality gates.
- When editing docs, keep `README.md` user-facing and keep `AGENTS.md` focused on agent-specific guidance and repo-specific expectations.

## Running a Single Test

Because this repo does not use pytest/unittest, "single test" means:

1. Validate one skill with `quick_validate.py`, or
2. Run one skill's `validate_examples.py` against its `examples.md`.

If you need one specific example case only, create a temporary minimal examples file and pass it via `--examples`. For exact command lines and examples format details, see `README.md`.

## Enforced Skill Metadata Rules

- `quick_validate.py` enforces YAML frontmatter, required `name` and `description` keys, restricted top-level metadata keys, and the naming/description constraints documented in `README.md`.

## Code Style Guidelines

### Imports

- Group imports by standard library, third-party, then local.
- Prefer explicit imports; avoid wildcard imports.

### Formatting

- Follow PEP 8 style (4-space indentation, readable line lengths).
- Keep script/module docstrings concise and accurate.
- Keep CLI usage examples runnable.

### Types

- Existing scripts are mostly untyped; follow local style in touched files.
- Add type hints only when they improve clarity and stay consistent.

### Naming

- Use `snake_case` for Python symbols.
- Use descriptive function names (`validate_skill`, `parse_examples`).
- Keep skill folder name and frontmatter `name` aligned.

### Error Handling

- Fail fast in CLI scripts with explicit non-zero exit codes.
- Print actionable error messages.
- Preserve existing behavior patterns (return tuple status vs exceptions) within each file.

### Paths and I/O

- Prefer `pathlib.Path` for path operations.
- Read/write text as UTF-8.
- Do not change archive path semantics in packager unless intentionally redesigning format.

## Validation Expectations Before Finishing

- Changes to skill metadata/content: run single-skill validation.
- Changes to skill smoke-test scripts or examples: run that skill's smoke tests.
- Changes to shared tooling (`.github/skills/skill-creator/scripts/`): run validation across multiple skills and packaging checks where relevant.
- Large or cross-cutting changes: run full validation loop + smoke-test loop.

## Copilot and Cursor Rule Coverage

- Guidance here is aligned with `.github/copilot-instructions.md`.
- No Cursor rules detected:
  - `.cursorrules` not present
  - `.cursor/rules/` not present

## Suggested Agent Workflow

1. Inspect target skill directory and related references/examples.
2. Make minimal, focused edits.
3. Run the smallest relevant validation command first.
4. Expand to broader loops only when scope requires it.
5. Report exactly which commands were run and their results.
