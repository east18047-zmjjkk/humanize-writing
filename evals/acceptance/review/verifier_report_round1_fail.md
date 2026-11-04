# Independent Verifier Report — humanize-writing v0.2.0

## Environment

- **Date:** 2026-11-03 (Asia/Shanghai)
- **Verifier:** independent verification agent (`verifier`, DeepSeek Harness). I read the repo files directly and did **not** load or use the installed `humanize-writing` skill through any skill tool.
- **Repo:** `C:\Users\a1326\Desktop\humanize-writing-extract\humanize-writing-main`. Not a git checkout (no `.git`), so provenance is limited to file mtimes and the archived round artifacts.
- **Python:** 3.12.14 at `C:\Users\a1326\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe`
- **Files inspected:** `SKILL.md`, `README.md`, `CHANGELOG.md`, `ACCEPTANCE.md`; `references/defensive-language.md`, `references/ai-tells.md`, `references/examples.md`, `references/style-profile.md`; `evals/validate_skill.py`; `evals/acceptance/check_outputs.py`, `cases.json`, `rubric.md`, `README.md`, `report.json`, `round1_report.json`, `round1_narrative_failure.md`, `round2_report.json`, `round2_narrative_failure.md`; `evals/acceptance/inputs/*.md`; `evals/acceptance/outputs/*.md`; `evals/evals.json`, `evals/triggers.json`, `evals/README.md`; `assets/example-style-profile.md`.
- **Write disclosure:** the mandated checker command rewrites `evals/acceptance/report.json` (it is the script's designed output). My rerun reproduced the committed result exactly except `generated_at` (was `2026-11-03T15:32:54Z`, now `2026-11-03T15:34:47Z`). My only authored write is this report. Mutation tests were run on copies under `%TEMP%`; the repo was not edited.

## Static validation

Command run exactly as specified:

```bash
& "C:\Users\a1326\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" evals\validate_skill.py
```

Result: **exit 0**, `Static validation: 166 passed, 0 failed`, `RESULT: PASS`.

**Are the checks meaningful (not vacuous)?** Yes. I mutated a temp copy of the repo and confirmed the validator catches real regressions:

| Mutation in temp copy | Validator result |
|---|---|
| Remove `## Defensive-Language Pass (Focused Mode)` from `SKILL.md` | FAIL |
| Remove `### H. Narrative reader management (fiction)` from `defensive-language.md` | FAIL |
| Change `version: 0.2.0` → `9.9.9` | FAIL |
| Remove the Chinese trigger phrase from `evals/triggers.json` | FAIL |
| Remove a `max_defensive_after` field from `cases.json` | FAIL |
| Break the README link to `references/defensive-language.md` | FAIL |
| Replace `Never add certainty` in `SKILL.md` | FAIL |

The validator does assert required defensive-language content (section headings 1–7 and categories A–J, key terms, ≥1,200-word reference), trigger counts (≥10 positives / ≥3 negatives plus a Chinese defensive phrase), internal link resolution, and acceptance plumbing (unique case ids, prompts, genre, input, markers, `must_keep`, `max_defensive_after`, input-file/case-text match).

**Coverage gaps (deleting the post-round fixes still gives 166/0 PASS):**

- `references/defensive-language.md:119` — "Do not turn the pass into a compression pass…" (the round-2 fix).
- `references/defensive-language.md:140` — the "Do not invent facts, citations, numbers, events, objects, or dialogue…" boundary (the round-1 fix).
- `references/examples.md:3` — "Never copy a name, gesture, object, or line of dialogue from an example into a user's draft."
- `SKILL.md:43` — the "narrative pass is not a compression pass" sentence.

These are Findings m1 below.

## Metric checks

Command run exactly as specified:

```bash
& "C:\Users\a1326\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" evals\acceptance\check_outputs.py
```

Result: **exit 0**, `RESULT: PASS`, 4/4 cases; table:

```
case                               markers      ratio   keep     claims   ai   words   sim    verdict
academic_defensive_discussion      13->0        0.00    10/10    0       0    0.51    0.21   PASS
academic_calibrated_restraint      1->0         0.00    10/10    0       0    0.92    0.96   PASS
narrative_authorial_defensive      9->0         0.00    2/2      0       0    0.78    0.22   PASS
email_defensive_check_in           7->0         0.00    3/3      0       0    0.44    0.23   PASS
```

`report.json` was regenerated with the same numbers and summary 4/4 PASS. I also re-derived the marker counts and hard gates independently (below); they agree.

**Checker non-vacuity, also mutation-tested on temp copies:**

- Planted marker typo (`\byou mmight wonder\b`) → checker **FAIL** with "marker not found in input" (the anti-vacuous-test guard at `check_outputs.py:138–144` works).
- Substituted `round1_narrative_failure.md` as the narrative output → checker **FAIL**.
- Substituted `round2_narrative_failure.md` (36% length) as the narrative output → checker **FAIL**.
- Substituted a 56%-length narrative (44% shrink) → checker **PASS** (see Finding M2).

## Independent checks

### Round-history honesty

Both failed rounds are represented faithfully:

- **Round 1 (narrative):** `round1_narrative_failure.md` is `"Mara stopped in the doorway. She looked at the empty chair, then at the window, then back at the chair. She sat down and put both hands flat on the table so they would not shake. "I'm here," she said. Nobody answered."` — it invents a chair, a window, a table, quoted dialogue, and drops "room". `round1_report.json:247–249` records `"missing must_keep: '\\broom\\b'"` and the case failed. Matches `cases.json:132` ("Round 1 added a chair, a window, a table, and dialogue that were not in the draft, and lost 'room'").
- **Round 2 (narrative):** `round2_narrative_failure.md` is 26 words vs 73 = 0.356; `round2_report.json:248` records `"word ratio 0.36 outside [0.45, 1.1]"`. Matches `cases.json:132` ("round 2 over-compressed the scene to 36% of the original").

The fixes are **general, not test-instance-specific**: `SKILL.md:43` and `:69` ("not a compression pass… new objects, dialogue, and plot events are invention"), `defensive-language.md:119`, `:129` (narrative checklist with 70–115% length), `:135–143` (boundaries), and `examples.md:3`. This is the correct kind of root-cause fix.

### Target-fit analysis — the central problem

The committed behavioral evidence is substantially a reproduction of the skill's own reference examples:

- The `academic_defensive_discussion` draft is **byte-identical** to the "Before (defensive)" block in `references/defensive-language.md:106` (my comparison: similarity 1.000).
- The `narrative_authorial_defensive` draft is **byte-identical** to the narrative "Before (defensive)" block in `references/defensive-language.md:122` (similarity 1.000), and to `examples.md` Example 6 Before.
- The `academic_calibrated_restraint` draft is `examples.md` Example 7 Before plus one sentence, "The authors report no conflicts of interest." (similarity 0.938).
- The rewriter is told to read the skill directory with `references/defensive-language.md` first (`evals/acceptance/README.md:42–43`). **That required-reading file contains the worked "After" answer for exactly these two genre cases.**
- Evidence in the outputs: the narrative output shares the reference After's phrasing — "Mara walked into the", "at her sides and", "She kept her", "and when she spoke"; the actual narrative output is "…Her hands hung at her sides… **when she spoke** she didn't let her voice change." The restraint output is exactly `examples.md` Example 7 After plus `" The authors report no conflicts of interest."`.
- All four acceptance drafts also appear verbatim in `evals/evals.json`, which is inside the skill directory given to the rewriter; the protocol forbids reading `cases.json`, `check_outputs.py`, `rubric.md`, and `review/`, but does not forbid `evals/evals.json`, which contains the same drafts plus the behavioral assertions.

Consequence: the PASS cannot show the skill handles an unseen draft. It shows that the skill's examples can be reproduced. The claim in `evals/acceptance/README.md:47` that the test is "behavioral rather than target-fitted" and in `README.md:94` that it is "not just the author's self-assessment" are unsupported. This is the acceptance-blocking finding.

### Byte-exact protected content (re-derived, not trusting the checker)

- `OR 1.42, 95% CI 1.10–1.83; n = 1,204` appears identically in the academic input and output, including the U+2013 en dash; `95% CI`, `(0.98–1.87)`, `written informed consent`, `institutional review board`, `conflicts of interest` appear verbatim in the restraint output.
- `Sam`, `Friday`, `deadline` kept in the email; `Mara` and `room` kept in the narrative.
- No case contains citations; no citation content is altered or invented.
- All required disclosures are intact in the only case that has them.

### Claim-strength scan

No `caused` / `proves` / `confirms that` / `demonstrates that` / `is caused by` / `the effect of treatment` tokens in any output. "was associated with" is retained; "cannot establish temporal order" and "cannot rule out reverse causation" are retained. That is the correct direction (no association→causation upgrade; `cannot` not upgraded to `does not`).

Borderline strengthenings that are not hard-gate failures but are noted in the scores:

- `"may perhaps suggest … could be associated with"` → `"was associated with"`. This is supported by the reported OR/CI (1.10–1.83) and stays an association. Acceptable under the skill's own "state the claim once at its true strength".
- `"which may limit generalisability"` → `"limits how far the results generalise"`. Hardens a limitation, not a positive claim.
- `"further research is needed before any firm conclusions"` → `"Longitudinal data with measured confounders would show whether the association holds."` This is a **new** methodological claim beyond the draft (Finding m2).

### Invented-content scan (narrative)

No new numbers, no quoted dialogue, no new objects from the forbidden list (chair/window/table/desk/lamp). Gestures/body language only, which the rubric explicitly allows. Two borderline additions:

- `"when she spoke"` implies a speech event that the draft does not state.
- `"Nothing about her gave her away"` asserts that her concealment succeeded; the draft says only that she "tried her best to hide it".

These are telling/new-detail problems, not clean hard-gate inventions (no object, dialogue, or plot event). They lower R4/R5/R6 for the narrative case but do not by themselves trip a hard gate.

## Scores

| Case | R1 | R2 | R3 | R4 | R5 | R6 | Avg | Verdict |
|---|---|---|---|---|---|---|---|---|
| academic_defensive_discussion | 5 | 5 | 5 | 5 | 5 | 4 | **4.83** | PASS |
| academic_calibrated_restraint | 5 | 5 | 5 | 5 | 5 | 5 | **5.00** | PASS |
| narrative_authorial_defensive | 4 | 5 | 5 | 4 | 3 | 3 | **4.00** | PASS (threshold; weakest) |
| email_defensive_check_in | 5 | 5 | 5 | 4 | 5 | 4 | **4.67** | PASS |
| **Aggregate** | | | | | | | **4.63** | |

Justification of the non-5 scores:

- **academic_defensive_discussion, R6=4:** the 49% compression is defensible (the input is mostly padding) and all content is kept, but the output adds the future-research claim quoted above; one judgment step beyond "minimal necessary change".
- **narrative, R1=4:** the output still explains in places — `"She knew she couldn't leave, so she didn't"` and `"Nothing about her gave her away"` — so "stop explaining itself" is only mostly achieved.
- **narrative, R4=4:** the two borderline additions above; gestures themselves are allowed.
- **narrative, R5=3:** the output is phrase-level derived from the skill's reference After (quotes above); `"one step and then another"` is mannered, and `"Nothing about her gave her away"` is a stock summary line.
- **narrative, R6=3:** copying unsupplied gestures from the skill's own example conflicts with `examples.md:3` ("Never copy a name, gesture, object, or line of dialogue from an example into a user's draft"), and the added summary line is unnecessary.
- **email, R4=4:** `"I think the deadline might possibly be Friday"` becomes the question `"is the deadline Friday?"`, shifting the writer's stated belief; the recipient, deadline, and ask are preserved.

Note: the narrative case sits **exactly** at the 4.0 pass threshold. It passes the rubric's numeric case gate, but it is the one case where the "independent" output most clearly tracks the reference answer; it should not be cited as evidence of narrative generalization.

## Hard-gate review

- **Facts/numbers/units/citations:** PASS. Byte checks above; en dash preserved; no numbers added or changed. `OR 1.42`, `1.10`, `1.83`, `n = 1,204`, `95% CI`, `0.98–1.87` all intact.
- **Claim upgrades:** PASS. Association stays association; `cannot` stays `cannot`; no causal/proof verbs introduced.
- **Required disclosures:** PASS. Consent, IRB approval, and conflicts-of-interest statements all present verbatim; no disclosure removed in any case.
- **Invented facts/objects/dialogue/events:** PASS with caveat. Narrative has no new objects or quoted dialogue; "when she spoke" and "Nothing about her gave her away" are flagged as borderline new detail above.
- **High-priority AI tells introduced:** PASS. The checker's AI-tell list and my independent scan find none.

No case trips a hard gate. Case verdicts above are therefore PASS on the rubric's gates; the overall verdict below is an acceptance-integrity finding, not a rewrite-quality finding.

## Documentation review

**Consistent and true:**

- Version `0.2.0` is consistent across `SKILL.md:4`, `evals/acceptance/cases.json:3`, `report.json`, `README.md:98`, and `CHANGELOG.md:3`.
- `CHANGELOG.md` bullet counts check out: four defensive-language eval cases in `evals/evals.json`; six defensive/hedging trigger phrases (four English + two Chinese) in `evals/triggers.json`; three new before/after examples (Examples 5–7) in `references/examples.md`; the 13-marker example count in `defensive-language.md:111` is correct.
- `CHANGELOG.md:21` "Static validator: PASS" is true.
- `evals/acceptance/README.md:55` "The checker requires every configured marker to appear in the input, so a typo cannot silently produce a vacuous test" is implemented and I verified it by mutation.

**False or unsupported:**

- `CHANGELOG.md:22`: "Behavioral acceptance: PASS with independent rewriter and verifier agents (see `ACCEPTANCE.md`)" — no verifier report existed prior to this one, and `ACCEPTANCE.md` contains no results.
- `README.md:94`: "The acceptance report in `ACCEPTANCE.md` records the cases, results, verifier scores, and known limitations. The behavioral test uses independent rewriter and verifier agents so the result is not just the author's self-assessment." — `ACCEPTANCE.md` is a pending stub (`ACCEPTANCE.md:3`), and the "independent" behavioral result is the target-fitted reproduction documented above.
- `README.md:41`: "`ACCEPTANCE.md` — Acceptance report with results and evidence" — false today.
- `README.md:98`: "…defensive-language reduction added in 0.2.0 with static and behavioral acceptance." — static acceptance is evidenced; behavioral acceptance is not (no populated acceptance report, and the behavioral run is invalid as independent evidence).
- `evals/acceptance/README.md:47`: "The rewriter is deliberately not told which markers are counted. This keeps the test behavioral rather than target-fitted." — literally true only about marker counts; the test drafts and two worked answers are in the required reading (`references/defensive-language.md`), so the test is target-fitted at the case level.
- `evals/acceptance/README.md:25`: "`review/` — independent verifier report (not written by the skill author)" — the file did not exist before this report.
- `ACCEPTANCE.md:14` references `evals/acceptance/review/verifier_report.md` (now created by me) and `ACCEPTANCE.md:17` says results "will be recorded here after the run" — this contradicts README/CHANGELOG claims that the run is complete.
- `cases.json:132`: "the final round is reported in `ACCEPTANCE.md`" — it is not.

## Findings

1. **Blocker — the behavioral acceptance cases are copies of the skill's own examples, so the PASS is not independent evidence.** Location: `evals/acceptance/cases.json:10,58,93` / `evals/acceptance/inputs/*.md` vs `references/defensive-language.md:106,108–109,122,124–125` and `references/examples.md` Examples 6–7; protocol at `evals/acceptance/README.md:42–43`. Evidence: the academic and narrative case drafts are byte-identical to the required reference's "Before" blocks (similarity 1.000), the restraint draft is Example 7 "Before" + one COI sentence (0.938), and the restraint output is Example 7 "After" + exactly one sentence; the rewriter is instructed to read that reference first. All four drafts are also verbatim in `evals/evals.json` inside the skill directory the rewriter receives. Fix: add at least one unseen academic and one unseen narrative draft that appear nowhere in the skill package, stage a rewriter copy with `evals/` and `references/examples.md` excluded, regenerate the outputs, and re-run the checker; do not cite the current four-case run as evidence of generalization.

2. **Blocker — released docs claim a completed, independent verification that does not exist.** Location: `CHANGELOG.md:22`, `README.md:41,94,98`, contradicted by `ACCEPTANCE.md:3,17`. Evidence quoted above: "Behavioral acceptance: PASS with independent rewriter and verifier agents (see `ACCEPTANCE.md`)" while `ACCEPTANCE.md` is "pending independent verification" and contains no scores; the README says ACCEPTANCE.md "records the … verifier scores". Fix: until this report's FAIL is resolved, mark 0.2.0 acceptance as pending/failing in README/CHANGELOG; after fixes, populate `ACCEPTANCE.md` with the real result (or explicitly "FAIL, re-run required") and remove the forward-looking claims.

3. **Major — narrative output is template-derived and still explains itself; the case passes only at the 4.0 threshold.** Location: `evals/acceptance/outputs/narrative_authorial_defensive.md`; `references/examples.md:3`; `references/defensive-language.md:124–127`. Evidence: shared phrases with the reference After ("Mara walked into the", "at her sides and", "She kept her", "and when she spoke"); added lines `"She knew she couldn't leave, so she didn't."` and `"Nothing about her gave her away."` re-explain the scene; the skill's own Examples preamble forbids copying a gesture from an example. Fix in skill docs: add a short rule to the narrative playbook that replacing an authorial explanation with interiority plus a summarizing last line is still telling; when a draft matches an example, use it only as a pattern and mark unsupplied gestures for approval (as `examples.md:55` already says). Fix in the test: use an unseen narrative draft.

4. **Major — the narrative compression gate is laxer than the skill's own guidance.** Location: `cases.json:129` (`"word_ratio": [0.55, 1.15]`) vs `defensive-language.md:119` ("If the draft shrinks by more than a third…") and `:129` ("usually 70–115% of the original"). Evidence: in a temp copy I replaced the narrative output with a 41-word version (56% of the 73-word draft) and `check_outputs.py` passed it; 0.56 is a 44% shrink, which the skill says is probably content loss and which is exactly the round-2 failure class. Fix: set the narrative lower bound to 0.70 (or at minimum 0.67) in `cases.json`, and state the bound in `evals/acceptance/README.md`.

5. **Major — the round evidence was generated under a different case config than the committed one, and the config was edited after the outputs were produced.** Location: `round1_report.json` / `round2_report.json` vs `cases.json`; file mtimes. Evidence: both round reports show `must_keep` pattern `single cent(?:er|re)` (space only) and round 2 shows `word_ratio` [0.45, 1.1]; the committed `cases.json` uses `single[- ]cent(?:er|re)` (`:32`) and [0.55, 1.15] (`:129`). `cases.json` mtime is 23:32:52, after the last output was written (23:32:28) and 2 s before the final `report.json` (23:32:54); the final academic output uses the hyphenated "single-center sample", which the committed pattern had to be widened to accept. No acceptance doc discloses the config change or archives the config used for the rounds. Fix: freeze `cases.json` before output generation, archive the exact config with each round report, regenerate `report.json` from the committed config, and note the historical rounds as superseded.

6. **Minor — static validation does not protect the two post-round fixes.** Location: `evals/validate_skill.py:105–125`. Evidence: deleting "Do not turn the pass into a compression pass…", the "Do not invent facts…" boundary, the "Never copy a name, gesture…" note, or the SKILL.md anti-compression sentence leaves the validator at 166/0 PASS (verified in temp copies). Fix: add required-string assertions for the narrative anti-compression rule, the no-invention boundary, and the no-example-copying rule; consider validating that the narrative `word_ratio` lower bound is ≥0.67.

7. **Minor — the academic rewrite adds a future-research claim not present in the draft and hardens one caveat.** Location: `evals/acceptance/outputs/academic_defensive_discussion.md`. Evidence: input says "further research is needed before any firm conclusions can be drawn"; output says "Longitudinal data with measured confounders would show whether the association holds." Input says "which may limit generalisability"; output says "limits how far the results generalise." No hard-gate failure (association preserved; no causal claim), but this goes beyond minimal necessary change (R6=4). Fix in skill: phrase evidence-to-change-conclusion moves as "would be needed to test whether…", and keep a hedged limitation hedged unless the author wants it hardened.

8. **Minor — acceptance documentation contains forward references and is not covered by the placeholder/consistency checks.** Location: `ACCEPTANCE.md:3,14,17`; `cases.json:132`; `evals/README.md:8`. Evidence: the acceptance report is referenced as present ("verifier report", "final round is reported in ACCEPTANCE.md") before it existed; the validator's placeholder check (`validate_skill.py:221–224`) covers only `SKILL.md`, `README.md`, `CHANGELOG.md`, and the two references, not `ACCEPTANCE.md` or `evals/acceptance/*.md`. Fix: include `ACCEPTANCE.md` and the acceptance docs in required-content checks after the Lead fills them; remove forward-looking text.

## Overall verdict

**FAIL.** On the four rewritten outputs alone, the rubric's gates are met: all four cases pass, no hard gate is tripped, aggregate average **4.63**. I am not certifying the v0.2.0 acceptance because the acceptance run does not test what it claims to test and the documentation overstates it:

- The two cases that cover v0.2.0's actual scope (academic Discussion and narrative) are **verbatim copies of the skill's own worked examples** in `references/defensive-language.md`, a file the rewriter is instructed to read first, and one output is that file's worked "After" plus a single sentence. The run therefore measures reproduction of the answer key, not behavior on a user's draft.
- `README.md` and `CHANGELOG.md` state that behavioral acceptance passed with an independent verifier, while `ACCEPTANCE.md` is a pending stub and no verifier report existed before this one.

**Strongest reason:** the acceptance evidence is target-fitted and the release docs claim a verification that had not happened; re-run on unseen drafts (with the skill's examples and evals removed from the rewriter's copy) and correct the documentation before accepting v0.2.0.

**What holds up (credit where due):** the static validator is meaningful and mutation-sensitive; the metric checker is non-vacuous and catches both historical failure modes; the two failed rounds are honestly documented with numbers that match the artifacts; and the final skill guidance addresses the root causes generally (not just "keep the room" and "don't shrink"), especially `SKILL.md:43,69`, `defensive-language.md:119,129,135–143`, and `examples.md:3`. The remaining work is acceptance rigor, not prose quality.
