# Archived Exploratory Rounds (Superseded)

These files are preserved for provenance. They are **not** acceptance evidence for v0.2.0.

Rounds 1–3 used drafts that were byte-identical or near-identical to the skill's own worked examples in `references/defensive-language.md` and `references/examples.md`. The independent verifier flagged this as target-fitted evidence: the run measured reproduction of the answer key rather than behavior on unseen drafts. The final acceptance uses four new drafts that appear nowhere in the skill package, generated from a blind copy of the skill (no `evals/`, no `examples.md`; the reference's section-4 worked examples remain, and this is disclosed in `ACCEPTANCE.md`).

What the rounds exposed and fixed:

| Round | Failure | Fix |
|-------|---------|-----|
| 1 | Narrative rewrite invented a chair, a window, a table, and dialogue; lost "room" | Added no-invention boundary and narrative information-conservation rule |
| 2 | Narrative rewrite compressed the scene to 36% of the draft | Added "a narrative pass is not a compression pass" guidance and 70–115% length check |
| 3 | Metrics passed after matcher corrections, but the drafts were copies of the worked examples | Replaced the entire acceptance set with unseen drafts and a blind protocol |
| 4 (pre-freeze) | First blind set passed content checks except one over-strict matcher (`cannot be ruled out` vs `cannot rule out`); tightening the case bounds changed `cases.json`, so the freeze was reset | Widened the matcher, set narrative floor to 0.67 and email floor to 0.20, then re-staged and re-ran the frozen set (`round4_prefreeze/`) |

`round1_report.json`, `round2_report.json`, `round3_report.json`, the two failure files, `old_cases_rounds1-3.json`, `round3_outputs/`, and `round4_prefreeze/` record the old outcomes and case/config hashes where available. The round-4 pre-freeze `cases.json` itself was not archived (only its hash in the blind manifest), and the archived round-3 report's `generated_at` is the verifier's re-run rather than the author's original. Round 1–3 reports predate case hashing. The final run is reported in `../../../ACCEPTANCE.md` and `../report.json`; its case file, hash chain, and blind manifest are complete.
