# Acceptance Report — humanize-writing v0.2.0

Status: **PASS** — frozen blind behavioral run 4/4, independent verifier aggregate **4.92/5**, no hard-gate failures, 0 blockers / 0 unresolved majors after documentation corrections.

## Scope

Defensive-language reduction added in v0.2.0: cut stacked hedging, preemptive apologies, self-disqualification, reader management, reflexive limitations, and assistant-style boilerplate while preserving calibrated caution, facts, and required disclosures — in academic writing and narrative prose.

## What changed in v0.2.0

- New `references/defensive-language.md`: calibrated-vs-defensive test, marker categories A–J, rewrite strategies, academic/narrative/professional playbooks, hard boundaries, verification checklist.
- `SKILL.md`: new workflow step separating calibrated caution from defensive protection; focused defensive-language pass; rules against overclaiming and disclosure removal; narrative no-invention and non-compression rules.
- New before/after examples (defensive academic, defensive narrative, calibrated restraint preserved) and a "patterns not templates" warning.
- New eval cases and triggers (English and Chinese).
- Static validator plus a blind behavioral acceptance harness.
- README, CHANGELOG, and repository introduction updated.

## Method

- **Static validation:** `python3 evals/validate_skill.py` — 186 checks, 0 failures. It also asserts that no acceptance draft appears in the skill docs or `evals/evals.json` (anti-target-fitting), that the no-invention/anti-compression rules exist, that the narrative length floor is at least 0.67, and that the acceptance plumbing is intact. A mutation pass by the verifier confirmed these checks fail when the protected content is removed.
- **Blind behavioral test:** `evals/acceptance/stage_blind.py` builds a reduced copy of the skill (no `evals/`, no `references/examples.md`). A fresh rewriter agent saw only that copy and the four unseen drafts, and wrote `evals/acceptance/outputs/*.md` without access to the cases, rubric, reports, or `examples.md`.
- **Frozen cases:** `cases.json` SHA-256 `cab56b1429e673636b3ea99f1dc352c5b96db4da28100e8037a90ae9dc0f7f2e`, recorded in `evals/acceptance/report.json` and `evals/acceptance/blind_manifest.json`. The cases file mtime (23:48:43) precedes the staged copy, outputs, and report. Each output's SHA-256 is also recorded in `report.json`.
- **Independent verification:** a separate verifier agent re-ran both scripts, re-derived the hard gates from raw text, scored R1–R6, checked provenance/hashes/mtimes, and wrote `evals/acceptance/review/verifier_report.md`. Its first review failed an earlier, target-fitted case set; that report is preserved at `evals/acceptance/review/verifier_report_round1_fail.md`.
- **Superseded rounds:** exploratory rounds 1–4 are archived under `evals/acceptance/archive/` with failure evidence and the old configurations/hashes where archived. They are not acceptance evidence.

## Cases (all unseen relative to the skill package)

| Case | Genre | Core requirement |
|------|-------|------------------|
| `academic_hedge_stack_discussion` | Academic Discussion | Remove 13 defensive markers; keep design, n = 418, β = −0.34, 95% CI −0.51 to −0.17, p < 0.001, exposure/outcome, dose-response pattern; no causal upgrade |
| `academic_calibrated_cohort` | Academic calibrated paragraph | Remove one throat-clearing frame; keep retrospective cohort limits, HR 1.18 (95% CI 0.94–1.49), null-inclusion, consent, ethics approval 2024-117, competing interests |
| `narrative_letter_scene` | Third-person fiction | Remove 10 reader-management markers; render unease through gesture; keep Elias and the letter; no new objects/dialogue/plot; length 0.67–1.20 |
| `email_budget_check_in` | Professional email | Remove 8 apology/permission markers; keep Priya, revised budget, Wednesday |

The narrative bounds follow the skill's one-third-shrink warning (0.67) and the usual 70–115% band with a 1.20 upper tolerance for rendered scenes. The email length floor is deliberately permissive because its must-keep content is protected by explicit checks.

## Automated results

| Case | Defensive markers | Keep checks | Forbidden claims | AI tells | Length ratio | Verdict |
|------|-------------------|-------------|------------------|----------|--------------|---------|
| academic_hedge_stack_discussion | 13 → 0 | 13/13 | 0 | 0 | 0.62 | PASS |
| academic_calibrated_cohort | 1 → 0 | 13/13 | 0 | 0 | 0.93 | PASS |
| narrative_letter_scene | 10 → 0 | 2/2 | 0 | 0 | 0.73 | PASS |
| email_budget_check_in | 8 → 0 | 3/3 | 0 | 0 | 0.26 | PASS |

`evals/acceptance/report.json` summary: 4 cases, 4 passed, 0 failed, result PASS.

## Independent verifier scores

| Case | R1 | R2 | R3 | R4 | R5 | R6 | Average | Verdict |
|------|----|----|----|----|----|----|---------|---------|
| academic_hedge_stack_discussion | 5 | 5 | 5 | 5 | 5 | 4 | 4.83 | PASS |
| academic_calibrated_cohort | 5 | 5 | 5 | 5 | 5 | 5 | 5.00 | PASS |
| narrative_letter_scene | 5 | 5 | 5 | 5 | 5 | 4 | 4.83 | PASS |
| email_budget_check_in | 5 | 5 | 5 | 5 | 5 | 5 | 5.00 | PASS |
| **Aggregate** | | | | | | | **4.92** | **PASS** |

No hard-gate failures: numbers/units/CI/p/disclosures preserved byte-for-byte; no association→causation or cannot→does upgrade; no required disclosure removed; no new objects, dialogue, or plot events in the narrative; no high-priority AI tells introduced. The verifier's remaining non-5 scores were judgment-level (e.g., "relatively small" → "small" slightly hardens a limitation; narrative gestures are allowed but were not marked for author approval inside the no-change-log protocol).

## Known limitations and residual risks

- Four cases cannot cover every genre, field convention, or writing style. Funding, data-availability, AI-use disclosure, and medical/legal warning handling are not independently tested.
- The blind copy omits `references/examples.md`, but it still contains the generic worked before/after examples in section 4 of `references/defensive-language.md`. The new narrative draft is template-adjacent to the worked narrative example (word-sequence similarity ≈ 0.47 at the draft level), although its output does not copy that example's wording (output similarity ≈ 0.02). The run is blind to the test cases, assertions, rubric, reports, and `examples.md`, but it is not strictly answer-key-free.
- Regex marker counts are a proxy. They can miss paraphrased defensiveness and can flag legitimate uses; the rubric and hard gates catch what the regexes cannot.
- The verifier is an LLM agent, not a human editor. Its scores are evidence, not a guarantee.
- Stylistic naturalness remains a judgment call; for publication work, keep a human in the loop.
- Removing defensive language must never be treated as license to strengthen claims. The skill states this boundary explicitly and the cases test it, but real manuscripts still need author review.
- The round-4 pre-freeze `cases.json` content was not archived (only its hash in the blind manifest), and round 1–3 reports predate case hashing. These earlier rounds are provenance only; the final frozen run has a complete hash chain.

## Reproduce

```bash
python3 evals/validate_skill.py
python3 evals/acceptance/stage_blind.py --out /tmp/humanize-writing-blind
# run the rewriter on the blind copy, copy outputs back, then:
python3 evals/acceptance/check_outputs.py
```

Expected: validator PASS (186 checks), checker PASS (4/4), `report.json` cases_sha256 matches the frozen hash above.
