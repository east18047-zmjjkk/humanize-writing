# Evals

This folder contains the static checks and behavior tests for the skill.

- `evals.json` — behavior test cases with expected assertions (including four defensive-language cases)
- `triggers.json` — routing tests: phrases that should and should not trigger the skill
- `validate_skill.py` — static validator for structure, frontmatter, links, required content, JSON shape, and acceptance plumbing
- `acceptance/` — full acceptance harness for the defensive-language feature (cases, rubric, protocol, metric checker, verifier report)

## Run the static checks

```bash
python3 evals/validate_skill.py
```

Exit code 0 means the skill package is structurally complete and the required defensive-language content is present.

## Run the behavior metrics

Generate outputs first following `acceptance/README.md`, then:

```bash
python3 evals/acceptance/check_outputs.py
```

This writes `acceptance/report.json` and exits 0 only if every case passes its machine checks.

## Adding cases

- Behavior case: add an entry to `evals.json` with `name`, `input`, and at least two `assertions`.
- Routing case: add an entry to `triggers.json` with `input` and `should_trigger`.
- Acceptance case: add a case to `acceptance/cases.json`, an input file under `acceptance/inputs/`, and run both scripts. Keep the assertions behavioral (what must be preserved or removed), not a hand-written expected answer.
