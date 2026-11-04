# Changelog

## 0.2.0 — 2026-11-03

### Added
- Defensive-language reduction, including a focused "defensive-language pass" mode for requests that only ask for less hedging/apology
- `references/defensive-language.md`: calibrated-vs-defensive test, marker inventory (categories A–J), rewrite strategies, academic/narrative/professional playbooks, hard boundaries, verification checklist
- Three new before/after examples in `references/examples.md` (defensive academic, defensive narrative, calibrated caution preserved)
- Four defensive-language eval cases in `evals/evals.json`
- Six defensive/hedging trigger phrases in `evals/triggers.json` (English and Chinese)
- `evals/validate_skill.py`: static validator (structure, frontmatter, links, required sections, eval JSON)
- `evals/acceptance/`: acceptance harness (cases, rubric, inputs, protocol, metric checker)
- `ACCEPTANCE.md`: acceptance report with evidence

### Changed
- `SKILL.md`: new workflow step separating calibrated caution from defensive protection; focused defensive-language pass; new key rules (never add certainty, never strip disclosures); resources and common-issues rows; version set to 0.2.0
- `README.md`: new introduction and defensive-language section, structure, install, usage, quality gates, and acceptance
- `references/ai-tells.md`: cross-reference to the defensive-language reference and genre notes

### Validation
- Static validator: PASS (186 checks, 0 failures)
- Frozen blind behavioral run: PASS on 4/4 unseen cases (13→0, 1→0, 10→0, and 8→0 defensive markers; all protected facts, disclosures, and claim-strength checks pass)
- Independent verifier review: PASS, aggregate 4.92/5, 0 blockers after documentation corrections (see `ACCEPTANCE.md`)

## 0.1.0 — 2026-11-03

- Initial skill creation
- Focus on English draft rewriting to remove AI tells
- Added support for persistent user style profile
- Included references for AI tells, style profiles, and examples
