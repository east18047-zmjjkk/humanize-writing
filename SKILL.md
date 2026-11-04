---
name: humanize-writing
description: "Rewrite drafts to remove AI tells, cut defensive hedging, and sound human. Use when editing text, removing AI flavor, reducing defensive or over-hedged language, humanizing writing, matching a user's style profile, or making papers/stories/prose sound natural."
version: 0.2.0
type: workflow
lifecycle: active
---

# Humanize Writing — Remove AI Flavor, Cut Defensive Language, Match Human Voice

Rewrite existing drafts so they sound like a person wrote them. Remove common AI tells and defensive language while preserving meaning, facts, and intent. Optionally match a persistent user style profile built from historical samples.

Use for papers, stories, emails, reports, or any prose that currently feels machine-generated or over-defensive. Primarily English.

## Core Workflow

1. **Check for style profile**
   - Look for an existing profile (see `references/style-profile.md`).
   - If none exists and the user has provided samples or the conversation history shows a consistent voice, offer to create one.
   - Load the profile before rewriting if available.

2. **Analyze the draft**
   - Scan for AI tells (see `references/ai-tells.md`).
   - Scan for defensive language (see `references/defensive-language.md`): stacked hedges, preemptive apologies, self-disqualification, meta-commentary, reader management, and reflexive limitations.
   - Note sentence-length uniformity, forced structures ("not X but Y"), throat-clearing openers, empty emphasis words, and overused metaphors.
   - Determine the genre (academic, narrative, professional, general) and the claim strength the evidence actually supports.
   - Identify what must be preserved: facts, numbers, citations, disclosures, core argument, required structure.

3. **Separate calibrated caution from defensive protection**
   - For every hedge or caveat, ask: does it tell the reader what is uncertain and why (keep), or does it only lower the writer's exposure (cut or rewrite)?
   - Keep evidence-linked uncertainty, real limitations, and required disclosures. Convert vague caveats into specific ones where possible.
   - Flag any edit that would strengthen a claim beyond the evidence. That is a factual change, not a style edit; do not make it silently.
   - If the text is already well calibrated, plan minimal edits or none.

4. **Rewrite**
   - Preserve meaning and information density. Do not invent facts or delete key points.
   - Remove or replace AI tells and defensive markers. Prefer plain, spoken-like verbs.
   - Vary sentence length deliberately (mix short and longer sentences).
   - Use contractions where they fit the formality level.
   - Add specificity and concrete language where the draft is abstract — but only from what the draft implies or the user supplies.
   - If a style profile exists, match its formality, rhythm, vocabulary preferences, and voice markers.
   - For academic papers: keep precision; one calibrated hedge per uncertain claim; cut formulaic hedging and significance inflation; never upgrade association to causation.
   - For stories: favor showing over telling; remove reader management and authorial apology; keep deliberate ambiguity and character voice. Render emotion with gestures and body language, never with new objects, dialogue, or plot events the draft does not state or imply. A narrative pass is not a compression pass: keep the scene's facts and its turn; if the draft shrinks by more than a third, you probably cut content rather than rendered it.
   - Read the result mentally aloud. It should not feel like it was optimized to avoid detection, and it should not feel like it is apologizing for existing.

5. **Verify and deliver**
   - Run the defensive-language verification checklist: marker count, protected facts, disclosures, calibration, no claim upgrade.
   - Provide the rewritten text.
   - Optionally list the main changes (markers removed, content preserved, anything flagged).
   - If the user edits or accepts, note any new style preferences and offer to update the profile.
   - Save or update the style profile persistently when appropriate.

## Defensive-Language Pass (Focused Mode)

When the request is only about sounding less defensive, over-hedged, apologetic, or "AI-written", run a dedicated pass instead of a full rewrite:

1. **Scan and tag** each defensive phrase with its category from `references/defensive-language.md` (A–J).
2. **Classify** it: cut, keep (calibrated or required), or rewrite as a specific statement.
3. **Rewrite in one pass.** Prefer deletion and specificity over synonym swaps. Never replace "may potentially" with "might perhaps".
4. **Verify** with the checklist: markers at least halved (or ≤2 per 500 words), protected facts intact, disclosures intact, no claim upgraded.
5. **Report briefly.** Example: "Removed 11 defensive markers; kept the cross-sectional limitation, the confidence interval, and all disclosures; no factual changes." If nothing needed cutting, say so.

## Key Rules

- **Calibration over confidence**: The goal is not to sound more certain. It is to keep uncertainty where the evidence is uncertain and state the claim everywhere else.
- **Never add certainty**: Do not turn "was associated with" into "caused", "suggests" into "proves", or a single study into a general claim. Stronger claims require stronger evidence and an explicit decision.
- **Never strip required disclosures**: Ethics approval, consent, conflicts of interest, funding, data availability, AI-use disclosure, medical/legal/safety warnings, and content warnings stay unless the user explicitly says the context does not require them. When unsure, keep and flag.
- **Minimal necessary change**: Fix AI flavor, defensive hedging, and rhythm. Do not rewrite for the sake of rewriting if a sentence is already natural.
- **Information conservation**: Never add unsupported claims, data, citations, or examples. In narrative, concrete rendering may use gestures and body language for emotions already stated, but new objects, dialogue, and plot events are invention, not style. Never remove necessary content.
- **Genre awareness**: Academic formality is fine; robotic formality is not. Narrative can be looser. Defensive language looks different in a limitations paragraph than in a character's voice.
- **Human interval, not anti-AI**: Occasional formal transitions, longer sentences, and honest caveats are normal. Do not force extreme variation, zero formal words, or zero hedging.
- **Profile first when available**: Style matching takes priority over generic "human" defaults once a profile exists.

## Resources

- `references/ai-tells.md` — Common English AI tells and preferred alternatives. Load when scanning or rewriting.
- `references/defensive-language.md` — Defensive-language taxonomy, calibrated-vs-defensive test, genre playbooks, boundaries, and verification checklist. Load for any "too defensive / too hedged / sounds like AI" request.
- `references/style-profile.md` — How to create, store, update, and apply a persistent user style profile.
- `references/examples.md` — Before/after pairs for general prose, academic, narrative, style matching, and defensive language.
- `evals/` — Test cases, trigger phrases, and acceptance harness (see `evals/README.md`).
- `assets/example-style-profile.md` — Sample style profile.

## Common Issues

| Problem | Fix |
|---------|-----|
| Rewrite still feels stiff | Increase sentence-length variation; cut remaining throat-clearing phrases; add one concrete detail. |
| Text sounds defensive or apologetic | Run the focused defensive-language pass; tag markers, keep calibrated caveats, cut the rest. |
| Academic limitations dominate | One paragraph, four moves (design limit, bias direction, what would change it, stop); no reflexive "further research". |
| Removing hedges creates overclaiming | Restore the original claim strength; keep one evidence-linked hedge and flag the boundary to the user. |
| Narrative explains itself | Delete reader management and authorial apology; render emotion as behavior; let the scene carry the meaning. |
| Too casual for the genre | Raise formality to match profile or context; keep precision for papers. |
| Lost meaning | Re-check against original; restore any dropped facts or nuances. |
| No style profile yet | Produce a solid human rewrite first, then ask for 1–2 sample texts to build the profile. |
| User wants even tighter | Offer a second pass focused only on cutting residual filler. |

When the task is pure generation of new content rather than rewriting a draft, still apply the same tell-avoidance, defensive-language, and style rules from the start.
