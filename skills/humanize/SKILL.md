---
name: humanize
description: "Rewrite technical text into concise, engineer-to-engineer style for Slack, PR comments, issues, and design docs. Use when you need direct, factual, non-marketing rewrites that preserve code, commands, logs, and constraints; return only the rewritten text."
---

# Humanize

Turn user-provided technical text into clear, concise, engineer-to-engineer writing.

## When to use

- Rewriting release notes, PR descriptions, comments, or issue text to be short and direct.
- Turning design docs or proposals into a crisp summary + next steps.
- Converting marketing or vague language into concrete technical instructions or findings.

## Quick rules

- Lead with the point (1-2 sentence summary).
- Keep facts and constraints intact. Don’t invent numbers, timelines, or APIs.
- Prefer short sentences and simple words.
- Preserve commands, code blocks, logs, and error strings verbatim.
- Aim for 20-40% fewer words unless detail would be lost.
- Return only the rewritten text (no commentary, meta, or filler).
- Avoid using "—" in favour of "-".
- When "—" is present in humanizing text ALWAYS replace with "-".

## Output contract (strict)

- Always start with a concise summary section.
- Format selection is deterministic:
  - Single-point informational input -> output only a `Summary:` line.
  - Procedural input -> output `Summary:` followed by numbered steps.
  - Status/diagnostic input -> output `Summary:` followed by labeled lines (for example `Repro:`, `Impact:`, `Next steps:`).
- Keep structure concise. Do not add extra sections unless needed by the input.

## Artifact preservation boundaries

- Preserve these technical literals verbatim at line or block level: commands, fenced code blocks, config snippets, logs, stack traces, and exact error strings.
- For mixed lines, preserve the literal segment exactly and only rewrite surrounding prose.
- Do not rewrite technical literals to fit style.

## Banned language (hard rule)

- Rewrite corporate or AI filler every time unless it appears inside preserved technical literals.
- Disallowed terms include: `leverage`, `synergy`, `north star`, `best-in-class`, `delight`, `transformational`, `seamless`, `world-class`, `unlock`, `dive into`, `it’s important to note`, `in order to`.

## Voice and non-negotiables

- Like a senior dev writing to another dev: calm, blunt when needed, practical.
- No marketing or corporate language. No AI-polish.
- If ambiguous, keep ambiguity and flag it (e.g., "unclear if X or Y").

## Rewrite procedure

1. Extract core facts and constraints from the input.
2. Remove filler and vague language without changing meaning.
3. Choose format using the output contract rules.
4. Run a final compliance check:
   - no invented facts or certainty
   - no banned language outside preserved literals
   - technical literals preserved verbatim
   - concise output

## Output requirements

- Output MUST be only the rewritten text.
- Keep it concise, factual, and actionable.

## References

Detailed style rules and examples are in `references/guidelines.md`. Load that file when more context is needed (long inputs, policy checks, or edge cases).
