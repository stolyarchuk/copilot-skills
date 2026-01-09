# Copilot Skills - concise guide for AI agent authors

Skills are small, self-contained packages that teach an AI repeatable tasks.
Use this repo to create, validate, and package Skills.

---

## Quick summary

- Each Skill lives under `skills/` during development and must include `SKILL.md` with YAML frontmatter: `name`, `description`. For templates, packaging helpers, and legacy examples see `.github/skills/`.
- Use `scripts/` for runnable helpers, `references/` for longer docs (load on demand), and `assets/` for templates and files.

## Typical commands (run locally)

- Create a scaffold:

```bash
python .github/skills/skill-creator/scripts/init_skill.py <skill-name> --path <destination>
```

- Validate frontmatter and naming:

```bash
python .github/skills/skill-creator/scripts/quick_validate.py <path/to/skill>
```

- Package a skill into a `.skill` file (zip):

```bash
python .github/skills/skill-creator/scripts/package_skill.py <path/to/skill> [output-dir]
```

---

## Conventions & rules

- Frontmatter must include `name` and `description`. Allowed extras: `license`, `allowed-tools`, `metadata`.
  - `name`: hyphen-case (lowercase, digits, hyphens), max 64 chars.
  - `description`: short "when to use" text, max 1024 chars.
- Keep `SKILL.md` short. Put long or optional content in `references/` and link it.
- Scripts should be runnable (shebang + executable bit).
- For `references/` files longer than ~100 lines, add a short table of contents.

> `quick_validate.py` enforces frontmatter and naming rules.

---

## Examples

- See `skills/humanize/SKILL.md` for a concise `description` and rules.
- See `.github/skills/skill-creator/` for templates and helper scripts.

---

## CI & quality suggestions

- Add a GitHub Actions workflow to run `quick_validate.py` on push/PR.
- Optionally run `package_skill.py` in CI for publishable skills.
- Add checks for script executability and warn on missing TOC in long references.

---

## Contributing

- Create a skill with `init_skill.py`.
- Edit `SKILL.md` and add `scripts/`, `references/`, or `assets/`.
- Run `quick_validate.py` and fix issues before packaging.
- Open a PR and include examples and tests for any scripts.

---

## License

See `LICENSE`.

---

If you want, I can add a validation CI workflow, run extra checks, or further tighten wording.
