---
name: humanize-writing
description: "Rewrite drafts to remove AI tells and sound human. Use when editing text, removing AI flavor, humanizing writing, matching a user's style profile, or making papers/stories/prose sound natural."
type: workflow
lifecycle: active
---

# Humanize Writing — Remove AI Flavor, Match Human Voice

Rewrite existing drafts so they sound like a person wrote them. Remove common AI tells while preserving meaning, facts, and intent. Optionally match a persistent user style profile built from historical samples.

Use for papers, stories, emails, reports, or any prose that currently feels machine-generated. Primarily English.

## Core Workflow

1. **Check for style profile**
   - Look for an existing profile (see `references/style-profile.md`).
   - If none exists and the user has provided samples or the conversation history shows a consistent voice, offer to create one.
   - Load the profile before rewriting if available.

2. **Analyze the draft**
   - Scan for AI tells (see `references/ai-tells.md`).
   - Note sentence-length uniformity, forced structures ("not X but Y"), throat-clearing openers, empty emphasis words, and overused metaphors.
   - Identify what must be preserved: facts, numbers, citations, core argument, required structure.

3. **Rewrite**
   - Preserve meaning and information density. Do not invent facts or delete key points.
   - Remove or replace AI tells. Prefer plain, spoken-like verbs.
   - Vary sentence length deliberately (mix short and longer sentences).
   - Use contractions where they fit the formality level.
   - Add specificity and concrete language where the draft is abstract.
   - If a style profile exists, match its formality, rhythm, vocabulary preferences, and voice markers.
   - For academic papers: keep precision; cut formulaic hedging and significance inflation.
   - For stories: favor showing over telling; avoid stock emotional beats.
   - Read the result mentally aloud. It should not feel like it was optimized to avoid detection.

4. **Deliver and refine**
   - Provide the rewritten text.
   - Optionally list the main changes (especially if the user wants transparency).
   - If the user edits or accepts, note any new style preferences and offer to update the profile.
   - Save or update the style profile persistently when appropriate.

## Key Rules

- **Minimal necessary change**: Fix AI flavor and rhythm. Do not rewrite for the sake of rewriting if a sentence is already natural.
- **Information conservation**: Never add unsupported claims, data, or examples. Never remove necessary content.
- **Genre awareness**: Academic formality is fine; robotic formality is not. Narrative can be looser.
- **Human interval, not anti-AI**: Occasional formal transitions or longer sentences are normal. Do not force extreme variation or zero formal words.
- **Profile first when available**: Style matching takes priority over generic "human" defaults once a profile exists.

## Resources

- `references/ai-tells.md` — Common English AI tells and preferred alternatives. Load when scanning or rewriting.
- `references/style-profile.md` — How to create, store, update, and apply a persistent user style profile.
- `references/examples.md` — Before/after pairs for general prose, academic, and narrative.

## Common Issues

| Problem | Fix |
|---------|-----|
| Rewrite still feels stiff | Increase sentence-length variation; cut remaining throat-clearing phrases; add one concrete detail. |
| Too casual for the genre | Raise formality to match profile or context; keep precision for papers. |
| Lost meaning | Re-check against original; restore any dropped facts or nuances. |
| No style profile yet | Produce a solid human rewrite first, then ask for 1–2 sample texts to build the profile. |
| User wants even tighter | Offer a second pass focused only on cutting residual filler. |

When the task is pure generation of new content rather than rewriting a draft, still apply the same tell-avoidance and style rules from the start.
