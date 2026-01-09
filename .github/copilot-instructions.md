# Copilot / AI Agent Instructions for this Repo

Purpose: Help AI coding agents be productive here by highlighting repository structure, developer workflows, and project-specific conventions.

## Quick orientation

- This repo hosts reusable "Skills" designed for AI agents. Each skill lives in its own folder and must include a `SKILL.md` with YAML frontmatter (`name` and `description`). See example: `.github/skills/humanize/SKILL.md`.
- Primary helper scripts are under `.github/skills/skill-creator/scripts/`:
  - `init_skill.py` — create a new skill scaffold
  - `quick_validate.py` — validate `SKILL.md` frontmatter and naming
  - `package_skill.py` — validate + package a skill into a `.skill` (zip) file

## Key conventions (must follow)

- SKILL frontmatter

  - Required fields: `name` (hyphen-case, a-z0-9-; max 64 chars), `description` (clear "when to use" text; max 1024 chars).
  - Allowed additional keys: `license`, `allowed-tools`, `metadata`.
  - Frontmatter must be the first section in `SKILL.md` and delimited with `---`.
  - `description` is the primary trigger text used by agents — include explicit trigger contexts (file types, user intents) here.
  - Examples and validation rules are enforced by `.github/skills/skill-creator/scripts/quick_validate.py`.

- Naming and structure

  - Skill folder name should match best practice hyphen-case naming (e.g., `humanize`, `pdf-editor`).
  - Recommended resource subfolders: `scripts/` (executable helpers), `references/` (docs to be loaded only when needed), `assets/` (templates, images — NOT loaded into context).
  - Scripts intended to be executed should be runnable (include shebang or documented command) and marked executable when appropriate.

- Progressive disclosure
  - Keep `SKILL.md` concise: metadata (frontmatter) is always visible; body is loaded only after triggering; large or detailed docs belong in `references/` and should be linked from `SKILL.md`.
  - For long reference files (100+ lines), include a short table of contents at the top.

## Typical workflows (commands agents should run)

- Create a new skill scaffold
  - `python .github/skills/skill-creator/scripts/init_skill.py <skill-name> --path <destination>`
- Quick validation of a skill
  - `python .github/skills/skill-creator/scripts/quick_validate.py <skill-folder>`
- Package for distribution
  - `python .github/skills/skill-creator/scripts/package_skill.py <skill-folder> [output-dir]`
  - Packaging runs validation first and fails if validation does not pass.

## Examples from this repo (use when writing/validating)

- Good frontmatter + trigger example: `.github/skills/humanize/SKILL.md` — concise `description` that explicitly lists "When to use" cases.
- Templates & scripts: `.github/skills/skill-creator/scripts/init_skill.py` shows the recommended template structure for `SKILL.md`, `scripts/`, `references/`, and `assets/`.

## Do / Don't (actionable, repo-specific)

- DO put deterministic or repeatedly executed logic into `scripts/` so agents can run them instead of re-writing code each time.
- DO place detailed schemata, API docs, or policies in `references/` and link them from `SKILL.md` (they are loaded only when needed).
- DO include concrete examples and realistic user requests in `SKILL.md` body — agents use examples to validate intent and outputs.
- DON'T put installation or long operational documentation into `SKILL.md` body (these belong in `references/` or external docs).
- DON'T change frontmatter keys or naming rules without updating `quick_validate.py`.

## Debugging & tests

- When a skill fails to package, run `quick_validate.py` locally to see specific validation errors.
- Confirm scripts run by executing them locally (e.g., `python scripts/example.py`).

## Notes about packaging

- Packager creates a `.skill` (zip) file containing the skill folder. The packaging script includes files relative to the skill's parent directory (so the zip preserves the skill folder name).

---

If any of these conventions are unclear or you want different behavior (e.g., additional frontmatter fields or CI checks), tell me what should change and I will iterate on this guidance.
