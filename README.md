# Humanize Writing

An agent skill that rewrites drafts to remove AI tells and sound human. Supports matching a persistent user style profile built from historical writing samples.

Primarily for English prose: papers, stories, emails, reports, or any text that currently feels machine-generated.

## What it does

- Scans for common AI writing tells (delve, tapestry, not-X-but-Y, uniform sentence length, throat-clearing openers, empty emphasis, etc.)
- Rewrites while preserving meaning, facts, and intent
- Varies sentence rhythm deliberately
- Prefers plain, spoken-like language
- Optionally loads and matches a persistent user style profile
- Handles academic and narrative genres differently

## Structure

- `SKILL.md` — Core workflow and rules
- `references/ai-tells.md` — English AI tells and preferred alternatives
- `references/style-profile.md` — How to create, store, and apply a style profile
- `references/examples.md` — Before/after pairs
- `evals/` — Test cases and trigger phrases
- `assets/example-style-profile.md` — Sample profile

## Usage

Tell the agent:

- "Rewrite this draft to remove the AI flavor"
- "Humanize this paragraph"
- "Edit this to match my usual writing style"
- "Make this academic section sound less AI-generated"

Provide 300–800 words of your own writing the first time so the agent can build a style profile. Later rewrites will match it automatically.

## Status

Created and self-tested November 2026. Validator passed. Focused on draft rewriting for English with optional persistent style matching.
