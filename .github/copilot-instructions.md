# Copilot / AI Agent Instructions for this Repo

Purpose: Make AI coding agents productive here by highlighting repository structure, concrete workflows, and project-specific conventions.

## Big picture

- Repository scope: this repo contains modular "Skills" under `skills/<skill-name>/`. Each skill is composed of:
  - `SKILL.md` (required): short metadata + core usage guidance
  - `references/` (optional): long-form docs, examples, guidelines (load only when needed)
  - `scripts/` (optional): runnable helpers, smoke-test runners (include shebang, be deterministic)
  - `assets/` (optional): binaries or templates
- Tooling: authoring and packaging helpers live in `.github/skills/skill-creator/` (use `init_skill.py`, `quick_validate.py`, `package_skill.py`). Follow the progressive-disclosure principle: keep `SKILL.md` concise and reference large content from `references/`.

## Essential commands (copy/paste)

- Initialize a skill template:

```bash
python .github/skills/skill-creator/scripts/init_skill.py my-new-skill --path skills/public
```

- Validate a skill locally (and in CI):

```bash
python .github/skills/skill-creator/scripts/quick_validate.py skills/my-skill
```

- Package a skill to a distributable `.skill` (zip):

```bash
python .github/skills/skill-creator/scripts/package_skill.py skills/my-skill [./dist]
```

- Run smoke tests for examples (per-skill):

```bash
python skills/<skill>/scripts/validate_examples.py --examples skills/<skill>/references/examples.md --runner "python skills/<skill>/scripts/mock_runner.py"
```

## Validation & frontmatter rules (explicit)

- `SKILL.md` must start with YAML frontmatter (`---`); required keys are:
  - `name`: hyphen-case (lowercase letters, digits, hyphens), max 64 chars, no leading/trailing hyphen or `--`
  - `description`: short trigger text, no `<` or `>`, max 1024 chars
- Allowed extra keys: `license`, `allowed-tools`, `metadata`
- `quick_validate.py` enforces these rules; run it before packaging or opening PRs.

## Smoke tests & runner contract

- `references/examples.md` must include `Input`/`Expected output` fenced code blocks; `validate_examples.py` parses and compares them.
- Runner contract: the `--runner` command must read from stdin and write the skill output to stdout; keep outputs deterministic.
- If whitespace differences are acceptable, run `validate_examples.py` with `--fuzzy`.

## Packaging details & ZIP layout

- The packager validates and zips the skill. Files are added with paths relative to the skill folder's parent, so the resulting ZIP contains `skills/<skill-name>/...`.
- Packaging errors usually stem from invalid frontmatter; fix with `quick_validate.py` and retry.

## Environment & dependencies

- Scripts use `#!/usr/bin/env python3`. Recommended Python: 3.8+.
- `quick_validate.py` requires `PyYAML` (`pip install pyyaml`). `validate_examples.py` uses only stdlib modules.

## CI & PR checklist (recommended)

- Run `quick_validate.py` on modified skill folders in PR CI.
- Run `validate_examples.py` for any skill with `references/examples.md`.
- Ensure new/changed `scripts/` are executable and deterministic, and `SKILL.md` frontmatter follows rules.
- Optionally run `package_skill.py` in CI for publishable skill builds (not mandatory for PRs).

## Project-specific patterns & examples

- Model `SKILL.md` after `skills/humanize/SKILL.md` (short and trigger-focused).
- Use `skills/cpp-modernize/references/guidelines.md` as the canonical example for style and citation patterns (cite cppreference where appropriate).
- Keep `SKILL.md` <= ~500 lines; place long docs in `references/` and link them.

---

If anything here is unclear or you'd like an example CI workflow or publish steps, tell me what to add and I will iterate.

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
