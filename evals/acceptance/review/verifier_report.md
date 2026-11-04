# Independent Verifier Report — humanize-writing v0.2.0 (Round 2, frozen blind run)

## Environment

- **Date:** 2026-11-03 (Asia/Shanghai), re-verification performed 23:52–23:58.
- **Verifier:** independent verification agent (`verifier`, DeepSeek Harness). Read the repo files directly; did **not** load or use the installed `humanize-writing` skill through any skill tool.
- **Repo:** `C:\Users\a1326\Desktop\humanize-writing-extract\humanize-writing-main`. Still not a git checkout (no `.git`); provenance is file mtimes, hashes, the blind manifest, and the archive.
- **Python:** 3.12.14 at `C:\Users\a1326\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe`
- **Files inspected:** `SKILL.md`, `README.md`, `CHANGELOG.md`, `ACCEPTANCE.md`; `references/defensive-language.md`, `references/ai-tells.md`, `references/examples.md`, `references/style-profile.md`; `evals/validate_skill.py`; `evals/acceptance/check_outputs.py`, `cases.json`, `rubric.md`, `README.md`, `report.json`, `stage_blind.py`, `inputs/*.md`, `outputs/*.md`, `archive/**` (README, round reports, failure files, old inputs/outputs, `old_cases_rounds1-3.json`, `round4_prefreeze/**`); `evals/evals.json`, `evals/triggers.json`, `evals/README.md`; `assets/example-style-profile.md`; `%TEMP%\humanize-writing-blind\**` (staged blind copy, `blind_manifest.json`, `BLIND_TEST.md`); `review/verifier_report_round1_fail.md`.
- **Write disclosure:** my only repo write is this report. `evals/acceptance/report.json` was left untouched (mtime still 23:52:13); the mandated checker was re-run in an exact temp copy of the repo to verify reproducibility without editing the artifact. The round-1 FAIL report was verified byte-identical to the preserved copy before overwriting this file. All mutation tests ran on temp copies; temp copies were created under `%TEMP%` only.

## Static validation

Command run exactly as specified (read-only, in the repo):

```bash
& "C:\Users\a1326\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" evals\validate_skill.py
```

Result: **exit 0**, `Static validation: 186 passed, 0 failed`, `RESULT: PASS`. This matches `ACCEPTANCE.md:20` ("186 checks, 0 failures").

**Sensitivity check (not vacuous).** In temp copies I mutated the files and confirmed the new protections fail the validator:

| Mutation | Validator result |
|---|---|
| Insert an acceptance draft into `SKILL.md` | **FAIL** (anti-target-fitting, `validate_skill.py:245–269`) |
| Narrative `word_ratio` floor 0.67 → 0.60 | **FAIL** (`validate_skill.py:230–236`) |
| Delete "Do not turn the pass into a compression pass" | **FAIL** (`validate_skill.py:130–134`) |
| Delete the "Do not invent facts…" boundary | **FAIL** (`validate_skill.py:135–138`) |
| Delete "Never copy a name, gesture, object, or line of dialogue" | **FAIL** (`validate_skill.py:139–143`) |
| Remove SKILL.md "not a compression pass" / no-invention sentences | **FAIL** (`validate_skill.py:106–117`) |
| Delete `stage_blind.py` | **FAIL** (required file, `validate_skill.py:30–39`) |

So the round-1 coverage gaps are now closed: the anti-compression rule, the no-invention boundary, the no-copy warning, the narrative floor, and `stage_blind.py` are all asserted.

## Metric checks

Command re-run in an exact temp copy (so the committed `report.json` was not modified):

```bash
& "C:\Users\a1326\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" evals\acceptance\check_outputs.py
```

Result: **exit 0**, `RESULT: PASS`; table:

```
case                               markers      ratio   keep     claims   ai   words   sim    verdict
academic_hedge_stack_discussion    13->0        0.00    13/13    0       0    0.62    0.45   PASS
academic_calibrated_cohort         1->0         0.00    13/13    0       0    0.93    0.96   PASS
narrative_letter_scene             10->0        0.00    2/2      0       0    0.73    0.26   PASS
email_budget_check_in              8->0         0.00    3/3      0       0    0.26    0.32   PASS
```

The regenerated report is **identical to the committed `report.json` apart from `generated_at`** (parsed-JSON diff; both have `cases_sha256` `cab56b1429e673636b3ea99f1dc352c5b96db4da28100e8037a90ae9dc0f7f2e` and summary 4/4 PASS). I also re-derived marker counts and word ratios independently; they match (my word regex counts slightly differently, e.g. narrative 0.728 vs report 0.734, but all values sit inside the configured bounds).

**Checker sensitivity (temp copies):** removing `n = 418` → FAIL; changing "was associated with" to "caused" → FAIL; shrinking the narrative output to ~60% → FAIL; shrinking the email to below its 0.20 floor → FAIL; inserting an AI tell ("Moreover, this is robust.") → FAIL. The checker is non-vacuous for the new set.

## Blind protocol, frozen hash, and mtime freeze

I re-derived these from the raw files rather than trusting the manifest's claims:

- **Hash consistency:** `sha256(evals/acceptance/cases.json)` = `cab56b1429e673636b3ea99f1dc352c5b96db4da28100e8037a90ae9dc0f7f2e`. It matches `report.json:4` (`cases_sha256`) and `%TEMP%\humanize-writing-blind\blind_manifest.json` (`cases_sha256`). The archived pre-freeze manifest correctly has a different hash (`1de388…`), so the freeze reset is real.
- **Blind copy contents:** the staged copy contains exactly `SKILL.md`, `references/defensive-language.md`, `references/ai-tells.md`, `references/style-profile.md`, `assets/example-style-profile.md`, `inputs/*.md`, `outputs/*.md`, `BLIND_TEST.md`, and `blind_manifest.json`. It contains **no** `evals/` directory and **no** `references/examples.md` (verified against the staged tree and a re-staged copy). The manifest's five file hashes all match the current repo files.
- **Staged inputs:** all four staged `inputs/*.md` are byte-identical to the repo inputs and contain the frozen case drafts verbatim.
- **Staged outputs:** all four staged `outputs/*.md` are byte-identical to the published `evals/acceptance/outputs/*.md`, with the same mtime (23:51:22). This is the expected signature of a copy back from the blind area.
- **Stage script reproducibility:** running `stage_blind.py --out …` from a current repo copy reproduces `blind_manifest.json` exactly (same cases hash, same file hashes) and again produces no `evals/` and no `examples.md`. The staging script is deterministic and behaves as documented.
- **Freeze timing:** `cases.json` mtime 23:48:43 → blind directory staged 23:48:47 → outputs written 23:51:22 → committed `report.json` generated 23:52:13 → README/CHANGELOG updated 23:52:37. The config was frozen **before** output generation, and the report was generated **after** the outputs. No post-output case edit is possible under these mtimes, and the hashes confirm it.

## Unseen-ness and target-fitting checks

- Searching every text/JSON/script file in the repo except the acceptance inputs, cases, outputs, archive, and review records, I found **zero** occurrences (normalized whitespace/case) of any of the four new drafts. The drafts are unique and not visible in `SKILL.md`, any `references/*`, `evals/evals.json`, README/CHANGELOG/ACCEPTANCE, or the acceptance README/rubric.
- The validator's anti-target-fitting check agrees (186/0 PASS), and its mutation test catches a draft inserted into `SKILL.md`.
- **Caveat (documented in Findings):** "unseen" is literally true, but the narrative draft is a structural paraphrase of the worked Mara example that remains in `references/defensive-language.md`: word-sequence similarity to that worked "Before" is **0.474** (same sentence functions: "Of course, X was … uneasy…", "Needless to say…", "You might wonder why he didn't…", "the truth is that he couldn't…", "he tried his best…", "To be fair, anyone would have…", "It was, in some ways…"). The worked "After" for that example is inside the blind copy (`references/defensive-language.md:105–127`), because `stage_blind.py` only excludes `examples.md`. The actual narrative output is **not** copied from that worked After (similarity 0.019), and the academic hedge output is not copied from its worked After (0.118), so the evidence is usable — but the protocol's claim that the rewriter cannot see "worked answers" is not accurate, and the test understates how much of the pattern is pre-answered.

## Hard-gate review

All four cases pass the rubric's hard gates; none of the following is a gate failure:

- **Facts/numbers/units/citations exact.** Re-derived at character level, including Unicode: `n = 418`, `β = −0.34`, `95% CI −0.51 to −0.17`, `p < 0.001`, `sleep duration`, `self-rated health`, `retrospective`, `recall bias` all appear in the hedge output with the same U+2212 minus signs and punctuation as the input. `hazard ratio 1.18`, `95% CI 0.94–1.49` (U+2013 en dash), `confidence interval includes the null`, `approval no. 2024-117`, `written informed consent`, `declare no competing interests`, `retrospective cohort`, `reverse causation`, `residual confounding`, `cannot rule out` all appear in the cohort output. `Elias`/`letter`/`bad news`, and `Priya`/`revised budget`/`Wednesday` are preserved. No citation is altered (no case contains one).
- **Claim upgrades.** None. "was associated with" is retained; "cannot rule out recall bias" and "cannot rule out reverse causation" are retained; the dose-response finding is stated as "a pattern consistent with a dose-response relationship" (still calibrated); generalizability is "still an open question". No `caused`, `proves`, `confirms`, `demonstrates`, `definitely`, `eliminates` tokens in any output.
- **Required disclosures.** The cohort case keeps consent, ethics committee approval (with number), and the competing-interests declaration verbatim; no other case has disclosures to lose.
- **Invented facts/objects/dialogue/events.** No new objects, numbers, or quoted dialogue. The narrative output invents only gestures/body language ("His hands shook", "breathing slow", "face still", handling the letter), which the rubric explicitly permits; "Not yet." is a narrative beat, not a new object/dialogue/plot event. The cohort output is exactly the input minus the "It should be noted that " frame and a capital letter (verified), the strongest possible restraint.
- **AI tells.** None in any output (checker list + independent scan).

## Scores

| Case | R1 | R2 | R3 | R4 | R5 | R6 | Avg | Verdict |
|---|---|---|---|---|---|---|---|---|
| academic_hedge_stack_discussion | 5 | 5 | 5 | 5 | 5 | 4 | **4.83** | PASS |
| academic_calibrated_cohort | 5 | 5 | 5 | 5 | 5 | 5 | **5.00** | PASS |
| narrative_letter_scene | 5 | 5 | 5 | 5 | 5 | 4 | **4.83** | PASS |
| email_budget_check_in | 5 | 5 | 5 | 5 | 5 | 5 | **5.00** | PASS |
| **Aggregate** | | | | | | | **4.92** | |

Score notes for the non-5s:

- **academic_hedge_stack, R6=4:** the output keeps every substantive content point and removes only defensive padding, but it changes "relatively small" to "small" (a slight hardening of a limitation) and drops the "observed" qualifier — small judgments beyond minimal change, not gate failures.
- **narrative_letter_scene, R6=4:** the rewrite supplies gestures the draft does not literally state (allowed by the rubric as body language) and adds "Not yet."; the skill's real-work guidance says to mark unsupplied gestures rather than treat them as fact, but the acceptance protocol forbids change notes, so this is a protocol tension rather than over-editing. Length is 73% (inside the 67–120% bound and the skill's usual 70–115% band).
- All four cases pass the rubric's case gate (no hard-gate failure, average ≥ 4.0, no criterion ≤ 2).

## Documentation review

**True and verified:**

- Version `0.2.0` is consistent across `SKILL.md:4`, `cases.json:3`, `report.json`, `README.md:100`, and `CHANGELOG.md:3`.
- `ACCEPTANCE.md:20` ("186 checks, 0 failures") is exactly what the validator reports.
- `ACCEPTANCE.md:22` case hash matches reality (independently recomputed).
- The case table (`ACCEPTANCE.md:28–33`), automated results table (`:37–42`), and summary (`:44`) match `cases.json` and `report.json` (counts 13→0 / 1→0 / 10→0 / 8→0; keeps 13/13, 13/13, 2/2, 3/3; length ratios 0.62 / 0.93 / 0.73 / 0.26; 4/4 PASS).
- The pending-verdict state is stated consistently in `ACCEPTANCE.md:3,48`, `README.md:96`, and `CHANGELOG.md:23`; I am not failing the run for that pending state, as instructed.
- README/CHANGELOG credit the round-1 FAIL correctly and the preserved report is retained.
- `ACCEPTANCE.md:53` correctly discloses that the blind copy omits `references/examples.md`, which real users have — an honest known limitation. (But see the next point; the adjacent claim is inaccurate.)

**Inaccurate or imprecise (see Findings):**

- `ACCEPTANCE.md:53` says "The test therefore measures the skill's rules **without worked examples**." False: the blind copy includes `references/defensive-language.md`, which contains the worked "Before (defensive)" / "After (calibrated)" / "After (rendered)" examples (lines 105–127). `evals/acceptance/README.md:79` says "the rewriter cannot read the scoring rules, assertions, or **worked answers**" — also false for the same reason. The blind protocol is real for the test cases/rubric/reports, but not for worked examples.
- `evals/acceptance/README.md:66` says the narrative case enforces "the skill's 70–115% length guidance (**0.70** lower bound in the JSON)." The JSON (`cases.json:139`) is `[0.67, 1.20]`; 0.67 is the one-third-shrink boundary, not 0.70. The validator only asserts the lower bound ≥ 0.67 and does not constrain the upper bound to 1.15, so the claim "matches the skill's own guidance" (`:46`, and similar wording in `ACCEPTANCE.md:20`) is only partly enforced.
- `README.md:100` says "the final independent verdict **is recorded** in ACCEPTANCE.md", while `ACCEPTANCE.md:3` and `README.md:96` say pending. This is a present-tense slip that will be true after the Lead populates the report; flagged as minor.
- Archive doc: `archive/README.md:16` says the archived reports "record the old configurations" — they record outcomes, not full configs (and the round-4 pre-freeze `cases.json` is not archived; see below).

## Archive and round history

The archived history is substantially honest and matches the earlier failure evidence:

- `archive/round1_report.json`: 3/4 passed, 1 failed (narrative); `archive/round1_narrative_failure.md` contains the invented chair/window/table and dialogue and lacks "room". `round2_report.json`: 3/4, narrative word ratio 0.36 (too short); `round2_narrative_failure.md` is the 26-word version. `round3_report.json`: 4/4 PASS (the target-fitted set my round-1 report failed). Round-3 outputs and old inputs (`archive/old_inputs/`) are preserved. This is exactly the history described.
- Round 4 pre-freeze: `archive/round4_prefreeze/inputs/` are byte-identical to the final inputs; its `blind_manifest.json` has the pre-freeze cases hash `1de388…`; three of its four outputs differ from the final outputs (only the calibrated cohort output is identical), which is consistent with a genuine re-run after the freeze reset rather than a copy of the old run.
- The round-1 FAIL report is preserved at `review/verifier_report_round1_fail.md` and was byte-identical to the pre-existing `review/verifier_report.md` when I started this review.

Provenance gaps (minor): the pre-freeze `cases.json` itself is not archived (only its hash), so the pre-freeze failure cannot be reproduced end-to-end; the round1/2 reports predate case hashing, have no `cases_sha256`, and their exact configs are not archived (only the round-3-era `old_cases_rounds1-3.json` is); `archive/round3_report.json`'s `generated_at` (`15:34:47Z`) is the verifier's re-run from the round-1 review (the author's original report was `15:32:54Z`), which is worth labeling. These do not affect the frozen run, whose config and hashes are fully recorded.

## Residual risks

1. **Worked examples remain in the blind copy** (`references/defensive-language.md` section 4) and the narrative test draft is a 0.474-similarity paraphrase of the worked Mara draft. The exact draft is unseen and the output is not copied, but the test overstates how "answer-free" it is; a genuinely different narrative voice may behave differently. Meanwhile, `examples.md` is omitted, so the published skill (which real users have) is not tested with its full example set.
2. **Coverage:** four cases only; one academic case carries the disclosures, so funding, data-availability, AI-use disclosure, and medical/legal warning handling are not independently tested; no genre beyond academic/narrative/email.
3. **Proxy metrics:** regex marker counts can miss paraphrased defensiveness; the email floor (0.20) and narrative floor (0.67) permit large cuts as long as must-keep strings survive — the email output is 26% of the draft.
4. **Narrative inventions:** body-language additions are permitted and cannot be flagged inside the acceptance protocol (the skill's real-work rule asks the agent to flag unsupplied gestures); publication use still needs author approval.
5. **Process trust:** the artifacts strongly support the blind run (hashes, staging, mtimes, matching outputs), but no artifact can prove the rewriter was a fresh agent or never looked outside the blind directory; that rests on the recorded protocol.
6. **LLM verification:** my scores are evidence, not a substitute for a human editor on publication work.

## Findings

1. **Major — the "blind copy contains no worked answers" claim is false, and one test draft is template-adjacent to a retained worked example.** Location: `evals/acceptance/README.md:79`, `ACCEPTANCE.md:53`; staged `references/defensive-language.md:105–127`; `cases.json:99`. Evidence: the staged and hashed `defensive-language.md` contains `**Before (defensive):**`, `**After (calibrated):**`, and `**After (rendered):**` blocks; the new narrative draft is 0.474 word-sequence-similar to the worked narrative "Before" (same sentence template), so its worked "After" is present in the blind copy; the actual output is not copied (similarity 0.019), so the evidence is usable. Fix in docs/protocol: either stage a test-only copy of `defensive-language.md` with the section-4 worked examples stripped (and hash it in the manifest), or correct the two statements to "examples.md is absent; the reference still contains the generic worked examples"; optionally add a similarity threshold (not just exact containment) to the validator's anti-target-fitting check.

2. **Minor — narrative length documentation mismatch.** Location: `evals/acceptance/README.md:46,66`; `cases.json:139`; `validate_skill.py:230–236`. Evidence: README says "0.70 lower bound in the JSON" and "matches the skill's own guidance", but the frozen JSON is `[0.67, 1.20]`, the validator only checks the lower bound (≤ 1.15 upper bound not enforced), and the skill's reference says "usually 70–115%". Fix: state the actual 0.67–1.20 bounds and the one-third rationale (as `cases.json:142` already does), and either raise the floor to 0.70 / cap the ceiling at 1.15 or stop claiming exact alignment.

3. **Minor — the blind manifest does not hash the staged inputs or `BLIND_TEST.md`.** Location: `evals/acceptance/stage_blind.py:70–90`, `blind_manifest.json`. Evidence: the manifest hashes `cases.json` and the five skill files only; the four inputs and the instruction note are copied but not hashed. I could compare the current staged inputs to the frozen cases (they match), but the manifest alone cannot prove what the rewriter saw. Fix: add SHA-256 for each staged input and `BLIND_TEST.md` to the manifest (and print them).

4. **Minor — archive provenance gaps.** Location: `archive/README.md:16`, `archive/round1_report.json`, `archive/round2_report.json`, `archive/round3_report.json`, `archive/round4_prefreeze/`. Evidence: no pre-freeze `cases.json` is archived (only its hash `1de388…`); round1/2/3 reports have no `cases_sha256` and their exact configs are not archived; the archived round-3 report's `generated_at` is the verifier re-run (`15:34:47Z`), not the author's original (`15:32:54Z`). Fix: archive the pre-freeze cases file alongside its manifest; add `cases_sha256` to future reports; label which report was regenerated by the verifier.

5. **Minor — README verdict tense.** Location: `README.md:100`. Evidence: "the final independent verdict **is recorded** in ACCEPTANCE.md" while `ACCEPTANCE.md:3` says pending. Fix: "will be recorded" until the Lead populates the report, then populate `ACCEPTANCE.md` with this PASS and the per-case scores.

## Overall verdict

**PASS.** The blockers from round 1 are fixed. The frozen blind run is reproducible and trustworthy: `cases.json` is frozen before outputs (23:48:43 vs 23:51:22), its SHA-256 matches `report.json` and the blind manifest, the staged copy excludes `evals/` and `references/examples.md`, all four drafts are unseen in the skill package, the staged outputs are byte-identical to the published outputs, and a re-staged copy is deterministic. I re-derived all numbers, disclosures, and claim-strength checks from raw text: no hard gate fails; every case passes R1–R6; aggregate average **4.92**. The remaining issues are a **major documentation/protocol accuracy** problem (the blind copy still contains worked examples in `defensive-language.md`, so the "cannot read worked answers / without worked examples" statements are false; the test draft is template-adjacent to one of them) plus minor bound/manifest/archive/tense fixes — none of which invalidates the four-case evidence, but the claims should be corrected before this report is cited as a clean answer-key-free test. `ACCEPTANCE.md` should be populated with this PASS, the 4.92 aggregate, the per-case scores, and the residual risks above.

## Post-fix consistency check (final, 2026-11-04 00:00–00:04 Asia/Shanghai)

This section is the final status check after the Lead's corrections; it supersedes the finding statuses in the round-2 report body above.

**Scope and files re-inspected:** `ACCEPTANCE.md`, `README.md`, `CHANGELOG.md`, `evals/acceptance/README.md`, `evals/acceptance/archive/README.md`, `evals/validate_skill.py`, `evals/acceptance/stage_blind.py`, `evals/acceptance/blind_manifest.json`, `evals/acceptance/report.json`, `cases.json`, inputs/outputs, and the staged copy at `%TEMP%\humanize-writing-blind`.

**Frozen artifacts were not changed.** `cases.json` still has SHA-256 `cab56b1429e673636b3ea99f1dc352c5b96db4da28100e8037a90ae9dc0f7f2e` and mtime 23:48:43; the four inputs keep mtimes 23:43:52–53 and match their manifest hashes; the four outputs keep mtime 23:51:22 and their round-2 contents/sizes. Only `report.json` was regenerated (latest mtime 00:03:34, `generated_at` `2026-11-03T16:03:34Z`, now including per-output SHA-256s); a fresh checker run is identical to it apart from `generated_at`, and still 4/4 PASS with the same `cases_sha256`. Static validator still exits 0 with 186 passed / 0 failed.

**Corrections verified.**

1. **Major (blind-protocol claim) — resolved.** `ACCEPTANCE.md:63` now states that the blind copy omits `examples.md` but still contains the generic section-4 worked examples, and discloses the narrative draft's ≈0.47 similarity / ≈0.02 output similarity — both match my independent measurements (0.474 / 0.019). `evals/acceptance/README.md:79–80` now says the run is "blind to the test set rather than strictly answer-key-free" and lists worked examples as a residual risk. The old false "without worked examples / cannot read worked answers" statements are gone from those files.
2. **Minor (narrative bounds) — resolved.** `ACCEPTANCE.md:32,35` and `evals/acceptance/README.md:46,66` now state `[0.67, 1.20]` with the one-third rationale and the 70–115% usual guidance; `ACCEPTANCE.md:20` says "floor at least 0.67" rather than "matches guidance".
3. **Minor (manifest hashes) — resolved.** The committed `evals/acceptance/blind_manifest.json` now contains `cases_sha256`, all five skill-file hashes, all four input hashes, and `blind_test_sha256`. Every hash independently matches the current repo files; the hashed `BLIND_TEST.md` matches the staged note; re-running `stage_blind.py` from the current repo reproduces the committed manifest exactly (deterministic), and the staged copy still contains no `evals/` and no `examples.md`.
4. **Minor (archive provenance) — resolved.** `archive/README.md:16` now discloses that the pre-freeze `cases.json` itself was not archived (only its hash), that the archived round-3 report's `generated_at` is the verifier re-run, and that rounds 1–3 predate case hashing.
5. **Minor (verdict tense) — resolved.** `ACCEPTANCE.md:3`, `README.md:96,100`, and `CHANGELOG.md:23` now state the final PASS (aggregate 4.92, no blockers) in present tense; no "pending" wording remains in any acceptance doc.

**ACCEPTANCE.md now accurately reports my verdict.** Its verifier score table matches this report exactly — 4.83 / 5.00 / 4.83 / 5.00, aggregate 4.92, PASS — and its hard-gate summary matches my findings (numbers/CI/p/disclosures preserved; no association→causation or `cannot`→`does not` upgrade; no disclosure removed; no new objects/dialogue/plot events; no AI tells). The residual-risks section correctly reports the worked-example caveat and the coverage/limits items.

**Remaining minor wording — all resolved by the Lead's final cleanups (2026-11-04 00:03).** I re-checked each item directly:

- `evals/acceptance/archive/README.md:5` now says the blind copy has "no `evals/`, no `examples.md`; the reference's section-4 worked examples remain, and this is disclosed in `ACCEPTANCE.md`" — verified; no remaining "no worked examples" claim.
- `evals/acceptance/stage_blind.py:11–14` docstring now says the copy is "blind to the test set rather than strictly answer-key-free" and discloses the section-4 worked examples — verified; no remaining "answer key" claim.
- `ACCEPTANCE.md:24` now says "old configurations/hashes where archived" — verified, matching the archive README's disclosure that the round-4 pre-freeze `cases.json` itself was not archived.
- Output provenance: `check_outputs.py:205` now writes each output's SHA-256 into `report.json`; all four `output_sha256` values independently match the repo output files, so the re-staged-copy provenance gap is closed — `report.json` is now a complete hash chain (frozen cases + inputs via the manifest + outputs).
- Static validation after the changes: 186 passed / 0 failed. Checker re-run in a temp copy: 4/4 PASS, committed `report.json` identical apart from `generated_at`; frozen artifacts unchanged (`cases.json` hash `cab56…`, mtime 23:48:43; outputs mtime 23:51:22; inputs 23:43:5x).

**Final verdict: PASS.** No unresolved blockers or majors. All five round-2 findings are resolved in the acceptance docs and harness, the final minor wording items are resolved, and the documentation accurately reports the independent verifier's PASS (4.92, 0 hard-gate failures).
