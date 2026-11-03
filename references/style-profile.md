# Style Profile Management

Maintain a persistent, lightweight style profile for the user so rewrites match their historical voice.

## What a Style Profile Contains

Keep it concise (under 300 words). Extract from user samples or conversation history:

- **Formality level**: casual / conversational / professional / academic
- **Sentence rhythm**: typical length range, preference for short punches vs long flowing sentences, burstiness
- **Vocabulary**: preferred word choices, avoided words, use of contractions, jargon tolerance
- **Voice markers**: humor, directness, hedging style, opinion strength, use of questions or asides
- **Structure habits**: paragraph length, transition style, opening/closing preferences
- **Genre adjustments**: how style shifts for papers vs stories vs emails (if samples show it)
- **Explicit preferences**: any "I always avoid X" or "I like to sound like Y" notes

Store as plain Markdown or a short structured note. Example:

```
Formality: conversational-professional
Rhythm: mix of 8-12 word sentences with occasional 25+ word ones; frequent short openers
Contractions: yes
Avoids: heavy business jargon, "delve", forced triads
Likes: concrete examples, mild dry humor, direct claims
Papers: more precise, fewer contractions, still avoids throat-clearing
```

## Creating / Updating a Profile

1. Ask for 300–800 words of the user's own writing (past emails, paper excerpts, stories, messages) or scan recent conversation history for consistent patterns.
2. Analyze for the traits above. Note what is *absent* as well as present (e.g., never uses "moreover").
3. Write the profile. Confirm key points with the user if uncertain.
4. Save it persistently:
   - Prefer a file the agent can re-read (e.g., `assets/user-style-profile.md` in the skill, or a user-specified path).
   - Or keep a short version in agent memory / conversation context for the session.
5. On subsequent rewrites, load the profile first and explicitly match its traits while still removing AI tells.

## Applying the Profile During Rewrite

- Match formality and contraction use.
- Mirror sentence-length variation patterns.
- Prefer vocabulary the user actually uses.
- Preserve the user's level of directness or hedging.
- Do not invent a personality the samples do not support.
- If the draft genre differs from samples (e.g., academic paper vs casual chat), adapt within the profile's range rather than forcing exact match.

## Updating Over Time

After a rewrite the user accepts or edits, note any new preferences ("user shortened the second paragraph further — prefers tighter endings") and append or revise the profile. Keep it current but not bloated.

If no profile exists yet, produce a solid human-sounding rewrite first, then offer to build one from the user's feedback or samples.
