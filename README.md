# Copilot Skills - concise guide for AI agent authors

[![skill validation](https://github.com/stolyarchuk/copilot-skills/actions/workflows/skill-validation.yml/badge.svg?branch=main)](https://github.com/stolyarchuk/copilot-skills/actions/workflows/skill-validation.yml) [![package skills](https://github.com/stolyarchuk/copilot-skills/actions/workflows/package-skills.yml/badge.svg?branch=main)](https://github.com/stolyarchuk/copilot-skills/actions/workflows/package-skills.yml)

Skills are small, reusable packages that teach an AI repeatable tasks. This repo explains how to author, validate, and package Skills.

## Contents

- `skills/cpp-modernize` - C++23 modernization: refactorings, short examples, and cppreference links. See `skills/cpp-modernize/SKILL.md`.
- `skills/cv-improver` - Recruiter-style CV critique + optional rewrite/re-review (no invention). See `skills/cv-improver/SKILL.md`.
- `skills/doca-expert` - DOCA Flow (>= 3.2.0): C++ patterns, performance trade-offs, and official links. See `skills/doca-expert/SKILL.md`.
- `skills/humanize` - Rewrite technical text into concise, engineer-to-engineer tone. See `skills/humanize/SKILL.md`.
- `skills/vpp-expert` - VPP/DPDK plugin architecture and C/C++ split guidance with references. See `skills/vpp-expert/SKILL.md`.

### Optional dependencies

- `skills/cv-improver`: if resumes are attached as PDFs and your agent runtime supports MCP tools, consider using MarkItDown via the markitdown-mcp server to convert documents to Markdown/text before critique/rewrite: <https://github.com/microsoft/markitdown>

---

## Quick summary

- Each skill lives in `skills/<name>/` and must include `SKILL.md` with YAML frontmatter: `name` and `description`.
- Use `scripts/` for runnable helpers, `references/` for long docs, and `assets/` for templates.

## Typical commands (run locally)

- Create a scaffold:

```bash
python .github/skills/skill-creator/scripts/init_skill.py <skill-name> --path <destination>
```

- Validate frontmatter and naming:

```bash
python .github/skills/skill-creator/scripts/quick_validate.py <path/to/skill>
```

- Package a skill:

```bash
python .github/skills/skill-creator/scripts/package_skill.py <path/to/skill> [output-dir]
```

---

## Conventions & rules

- `SKILL.md` must include `name` and `description`. Allowed extras: `license`, `allowed-tools`, `metadata`.
- `name` must be hyphen-case (lowercase, digits, hyphens), max 64 chars.
- `description` should be short (max 1024 chars).
- Keep `SKILL.md` short; move long or optional content to `references/`.
- Scripts must be runnable (shebang + executable bit).
- Add a small TOC to `references/` files longer than ~100 lines.

`quick_validate.py` enforces frontmatter and naming rules.

---

## Examples

- See `skills/humanize/SKILL.md` for a compact example.
- See `.github/skills/skill-creator/` for templates and helpers.

---

## CI & quality suggestions

- Add a GitHub Actions job to run `quick_validate.py` on push/PR.
- Optionally run `package_skill.py` in CI to build `.skill` artifacts.
- Add check for script executability and a TOC warning for long references.

---

## Contributing

- Create a skill with `init_skill.py`.
- Edit `SKILL.md` and add `scripts/`, `references/`, or `assets/`.
- Run `quick_validate.py` and fix issues before packaging.
- Open a PR and include examples or tests for scripts.

---

## License

See `LICENSE`.
