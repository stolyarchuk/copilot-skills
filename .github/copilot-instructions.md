# Copilot / AI Agent Instructions (copilot-skills)

This repo is a collection of modular “Skills” under `skills/<skill-name>/`.

## Skill layout (the contract)

- `skills/<name>/SKILL.md` (required): YAML frontmatter + short, trigger-focused usage guidance.
- `skills/<name>/references/` (optional): long-form docs, guidelines, examples.
- `skills/<name>/scripts/` (optional): deterministic helpers and smoke-test runners (use `#!/usr/bin/env python3`, set executable bit when appropriate).
- `skills/<name>/assets/` (optional): templates/binaries not meant to be loaded into context.

## Frontmatter rules (enforced)

- `SKILL.md` MUST start with YAML frontmatter (`---`). Required keys: `name`, `description`.
- `name`: hyphen-case `[a-z0-9-]`, max 64 chars, no leading/trailing `-`, no `--`.
- `description`: max 1024 chars, must not contain `<` or `>`.
- Only these top-level keys are allowed: `name`, `description`, `license`, `allowed-tools`, `metadata`.

## Authoring + validation workflows

- Scaffold a new skill:
  - `python .github/skills/skill-creator/scripts/init_skill.py my-new-skill --path skills`
- Validate a skill (same check CI runs):
  - `python .github/skills/skill-creator/scripts/quick_validate.py skills/<name>`
- Package to a distributable `.skill` (zip) into `dist/`:
  - `python .github/skills/skill-creator/scripts/package_skill.py skills/<name> ./dist`
  - ZIP paths are relative to the skill’s parent, so archives contain `skills/<name>/...`.

## Smoke tests (examples.md)

- If `skills/<name>/references/examples.md` exists, run:
  - `python skills/<name>/scripts/validate_examples.py --examples skills/<name>/references/examples.md --runner "python skills/<name>/scripts/mock_runner.py"`
- `examples.md` format is `Input:` / `Expected output:` fenced `text` blocks; the runner must read stdin and write stdout.

## Where to look for patterns

- Minimal, well-shaped `SKILL.md`: `skills/humanize/SKILL.md`.
- Citation/style-heavy references: `skills/cpp-modernize/references/guidelines.md`.
- CI sources of truth: `.github/workflows/skill-validation.yml` and `.github/workflows/package-skills.yml`.

## Dependencies

- Python 3.x.
- `quick_validate.py` requires `pyyaml` (CI installs it via `pip install pyyaml`).
