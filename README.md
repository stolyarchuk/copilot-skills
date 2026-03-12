# Copilot Skills

[![skill validation](https://github.com/stolyarchuk/copilot-skills/actions/workflows/skill-validation.yml/badge.svg?branch=main)](https://github.com/stolyarchuk/copilot-skills/actions/workflows/skill-validation.yml) [![package skills](https://github.com/stolyarchuk/copilot-skills/actions/workflows/package-skills.yml/badge.svg?branch=main)](https://github.com/stolyarchuk/copilot-skills/actions/workflows/package-skills.yml)

Skills are small, reusable packages that teach an AI repeatable tasks. This repo contains reusable skills plus the scripts and workflows used to validate and package them.

## Contents

- `skills/cpp-modernize` - C++23 modernization: refactorings, short examples, and cppreference links. See `skills/cpp-modernize/SKILL.md`.
- `skills/cv-adapter` - Recruiter-style resume adaptation to a specific job description (minimal edits, no invention). See `skills/cv-adapter/SKILL.md`.
- `skills/cv-improver` - Recruiter-style CV critique + optional rewrite/re-review (no invention). See `skills/cv-improver/SKILL.md`.
- `skills/doca-expert` - DOCA Flow (>= 3.2.0): C++ patterns, performance trade-offs, and official links. See `skills/doca-expert/SKILL.md`.
- `skills/humanize` - Rewrite technical text into concise, engineer-to-engineer tone. See `skills/humanize/SKILL.md`.
- `skills/position-screening` - Recruiter-style screening questions and evidence-based pre-screen analysis for a specific role and CV. See `skills/position-screening/SKILL.md`.
- `skills/screening-receiver` - Recruiter-style evaluation of completed screening answers with ranking and next-step recommendation. See `skills/screening-receiver/SKILL.md`.
- `skills/vpp-expert` - VPP/DPDK plugin architecture and C/C++ split guidance with references. See `skills/vpp-expert/SKILL.md`.

### Optional dependencies

- `skills/cv-adapter` / `skills/cv-improver`: if resumes are attached as PDFs and your agent runtime supports MCP tools, consider using MarkItDown via the markitdown-mcp server to convert documents to Markdown/text before critique/rewrite: <https://github.com/microsoft/markitdown>

---

## Repo layout

- Each skill lives in `skills/<name>/` and must include `SKILL.md` with YAML frontmatter: `name` and `description`.
- Use `scripts/` for runnable helpers, `references/` for long docs, and `assets/` for templates.

## Environment

- Python `3.x`
- Validator dependency: `pyyaml`

```bash
python -m pip install --upgrade pip
pip install pyyaml
```

Optional virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pyyaml
```

## Common local commands

- Create a scaffold:

```bash
python .github/skills/skill-creator/scripts/init_skill.py <skill-name> --path <destination>
```

- Validate frontmatter and naming:

```bash
python .github/skills/skill-creator/scripts/quick_validate.py skills/<skill-name>
```

- Validate all skills (validation portion of CI):

```bash
for d in skills/*; do
  if [ -f "$d/SKILL.md" ]; then
    python .github/skills/skill-creator/scripts/quick_validate.py "$d"
  fi
done
```

- Smoke test one skill with examples:

```bash
python skills/<skill-name>/scripts/validate_examples.py \
  --examples skills/<skill-name>/references/examples.md \
  --runner "python skills/<skill-name>/scripts/mock_runner.py"
```

- Smoke test all skills with examples:

```bash
for d in skills/*; do
  if [ -f "$d/references/examples.md" ] && [ -f "$d/scripts/validate_examples.py" ] && [ -f "$d/scripts/mock_runner.py" ]; then
    python "$d/scripts/validate_examples.py" \
      --examples "$d/references/examples.md" \
      --runner "python $d/scripts/mock_runner.py"
  fi
done
```

Run both loops to mirror the checks in `.github/workflows/skill-validation.yml`.

- Package a skill:

```bash
python .github/skills/skill-creator/scripts/package_skill.py skills/<skill-name> ./dist
```

- Package all skills:

```bash
mkdir -p dist
for d in skills/*; do
  if [ -f "$d/SKILL.md" ]; then
    python .github/skills/skill-creator/scripts/package_skill.py "$d" ./dist
  fi
done
```

---

## Metadata and authoring rules

- `SKILL.md` must include `name` and `description`. Allowed extras: `license`, `allowed-tools`, `metadata`.
- `name` must be lowercase hyphen-case, with no leading/trailing `-`, no `--`, max 64 chars.
- `description` must be at most 1024 chars and must not include `<` or `>`.
- Keep `SKILL.md` short; move long or optional content to `references/`.
- Scripts must be runnable (shebang + executable bit).
- Add a small TOC to `references/` files longer than ~100 lines.
- If `references/examples.md` exists, its format is `Input:` / `Expected output:` fenced `text` blocks, and the runner should read stdin and write stdout.

`quick_validate.py` enforces frontmatter and naming rules.

---

## Patterns and references

- See `skills/humanize/SKILL.md` for a compact example.
- See `.github/skills/skill-creator/` for templates and helpers.

---

## CI workflows

- `.github/workflows/skill-validation.yml` validates every skill on push/PR and runs smoke tests for skills that include examples.
- `.github/workflows/package-skills.yml` packages all skills on `main` pushes, supports manual runs with `workflow_dispatch`, and uploads `.skill` artifacts.
- `package_skill.py` preserves paths relative to the skill parent, so packaged archives contain `skills/<name>/...`.

---

## Contributing

- Create a skill with `init_skill.py`.
- Edit `SKILL.md` and add `scripts/`, `references/`, or `assets/`.
- Run `quick_validate.py`, and run smoke tests when the skill includes examples.
- Open a PR and include examples or tests for scripts.

---

## License

See `LICENSE`.
