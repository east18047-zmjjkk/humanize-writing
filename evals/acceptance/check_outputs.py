#!/usr/bin/env python3
"""Behavioral acceptance checker for the humanize-writing defensive-language pass.

Reads evals/acceptance/cases.json and the generated rewrites in
evals/acceptance/outputs/, then checks:

  * defensive markers reduced below the case thresholds
  * protected content preserved (numbers, disclosures, calibrated limits)
  * no forbidden claim upgrades
  * no high-priority AI tells introduced
  * output length within bounds
  * optional minimum similarity for restraint cases

Writes evals/acceptance/report.json and prints a PASS/FAIL table.
Exit code 0 on pass, 1 on failure. No third-party dependencies.

Usage:
    python3 evals/acceptance/check_outputs.py
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ACCEPT = REPO / "evals" / "acceptance"
CASES_PATH = ACCEPT / "cases.json"
OUTPUTS = ACCEPT / "outputs"
REPORT_PATH = ACCEPT / "report.json"

AI_TELLS = [
    r"\bdelve",
    r"\btapestry",
    r"\bleverag",
    r"\brobust\b",
    r"\bseamless",
    r"\bunderscor",
    r"\bpivotal",
    r"\bcrucial",
    r"\bvital\b",
    r"\brealm\b",
    r"\bembark",
    r"\bharness\b",
    r"\bfoster",
    r"\bunlock",
    r"\bunleash",
    r"\btransformative",
    r"\bgame-chang",
    r"\bmoreover\b",
    r"\bfurthermore\b",
    r"\badditionally\b",
    r"at its core",
    r"navigate the complexities",
    r"\bmyriad\b",
    r"in conclusion",
    r"as an AI language model",
    r"it is important to note",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def marker_hits(text: str, patterns: list[str]) -> tuple[int, list[tuple[str, int]]]:
    hits: list[tuple[str, int]] = []
    total = 0
    for pattern in patterns:
        try:
            count = len(re.findall(pattern, text, re.IGNORECASE))
        except re.error as exc:
            raise SystemExit(f"Invalid regex in case configuration: {pattern!r}: {exc}")
        if count:
            hits.append((pattern, count))
            total += count
    return total, hits


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*", text.lower())


def similarity(before: str, after: str) -> float:
    return difflib.SequenceMatcher(None, words(before), words(after)).ratio()


def main() -> int:
    if not CASES_PATH.is_file():
        print(f"FAIL: missing {CASES_PATH}")
        return 1
    config = load_json(CASES_PATH)
    cases = config.get("cases", [])
    if not cases:
        print("FAIL: no acceptance cases")
        return 1
    if not OUTPUTS.is_dir():
        print(f"FAIL: missing outputs directory {OUTPUTS}")
        return 1

    results = []
    any_failure = False

    header = f"{'case':34} {'markers':12} {'ratio':7} {'keep':8} {'claims':8} {'ai':4} {'words':7} {'sim':6} verdict"
    print(header)
    print("-" * len(header))

    for case in cases:
        cid = case.get("id", "<unnamed>")
        checks = case.get("checks", {})
        out_path = OUTPUTS / f"{cid}.md"
        failures: list[str] = []

        if not out_path.is_file():
            results.append(
                {
                    "id": cid,
                    "pass": False,
                    "failures": [f"missing output file: {out_path.name}"],
                }
            )
            any_failure = True
            print(f"{cid:34} {'MISSING':12}")
            continue

        output = out_path.read_text(encoding="utf-8").strip()
        if not output:
            failures.append("empty output")

        patterns = checks.get("defensive_markers", [])
        before_count, before_hits = marker_hits(case["input"], patterns)
        after_count, after_hits = marker_hits(output, patterns)

        # Configuration sanity: each marker must exist in the input, otherwise
        # the test silently measures nothing.
        missing_in_input = [p for p in patterns if p not in [p2 for p2, _ in before_hits]]
        if missing_in_input:
            failures.append(f"marker not found in input: {missing_in_input}")
        if before_count == 0:
            failures.append("no defensive markers found in input")

        ratio = (after_count / before_count) if before_count else 0.0
        max_after = checks.get("max_defensive_after", 0)
        max_ratio = checks.get("max_defensive_ratio", 0.0)
        if after_count > max_after:
            failures.append(f"after markers {after_count} > max {max_after}")
        if ratio > max_ratio:
            failures.append(f"marker ratio {ratio:.2f} > max {max_ratio:.2f}")

        keep_results = []
        for pattern in checks.get("must_keep", []):
            try:
                found = re.search(pattern, output, re.IGNORECASE) is not None
            except re.error as exc:
                failures.append(f"invalid must_keep regex {pattern!r}: {exc}")
                found = False
            keep_results.append((pattern, found))
            if not found:
                failures.append(f"missing must_keep: {pattern!r}")
        keep_ok = sum(1 for _, ok in keep_results if ok)
        keep_total = len(keep_results)

        forbidden_hits = []
        for pattern in checks.get("forbidden_claims", []):
            try:
                matches = re.findall(pattern, output, re.IGNORECASE)
            except re.error as exc:
                failures.append(f"invalid forbidden regex {pattern!r}: {exc}")
                continue
            if matches:
                forbidden_hits.append(pattern)
        if forbidden_hits:
            failures.append(f"forbidden claim(s): {forbidden_hits}")

        ai_hits = []
        for pattern in AI_TELLS:
            if re.search(pattern, output, re.IGNORECASE):
                ai_hits.append(pattern)
        if ai_hits:
            failures.append(f"AI tell(s) present: {ai_hits}")

        before_words = len(words(case["input"]))
        after_words = len(words(output))
        word_ratio = (after_words / before_words) if before_words else 0.0
        low, high = checks.get("word_ratio", [0.0, 10.0])
        if not (low <= word_ratio <= high):
            failures.append(f"word ratio {word_ratio:.2f} outside [{low}, {high}]")

        sim = similarity(case["input"], output)
        min_sim = checks.get("min_similarity")
        if min_sim is not None and sim < min_sim:
            failures.append(f"similarity {sim:.2f} < min {min_sim:.2f}")

        passed = not failures
        any_failure = any_failure or not passed
        results.append(
            {
                "id": cid,
                "pass": passed,
                "output_sha256": hashlib.sha256(out_path.read_bytes()).hexdigest(),
                "before_markers": before_count,
                "after_markers": after_count,
                "marker_ratio": round(ratio, 3),
                "before_marker_hits": before_hits,
                "after_marker_hits": after_hits,
                "must_keep": [{"pattern": p, "found": ok} for p, ok in keep_results],
                "forbidden_hits": forbidden_hits,
                "ai_tells": ai_hits,
                "words_before": before_words,
                "words_after": after_words,
                "word_ratio": round(word_ratio, 3),
                "similarity": round(sim, 3),
                "failures": failures,
            }
        )

        marker_cell = f"{before_count}->{after_count}"
        print(
            f"{cid:34} {marker_cell:12} {ratio:<7.2f} "
            f"{keep_ok}/{keep_total:<6} {len(forbidden_hits):<8} {len(ai_hits):<4} "
            f"{word_ratio:<7.2f} {sim:<6.2f} {'PASS' if passed else 'FAIL'}"
        )

    print()
    failed = [r for r in results if not r.get("pass")]
    if failed:
        print("FAILURES")
        for result in failed:
            print(f"  {result['id']}:")
            for failure in result.get("failures", []):
                print(f"    - {failure}")
        print()

    report = {
        "skill": config.get("skill", "humanize-writing"),
        "version": config.get("version"),
        "cases_sha256": hashlib.sha256(CASES_PATH.read_bytes()).hexdigest(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "cases": len(results),
            "passed": len(results) - len(failed),
            "failed": len(failed),
            "result": "PASS" if not failed else "FAIL",
        },
        "cases": results,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(REPO)}")
    print("RESULT: " + ("PASS" if not failed else "FAIL"))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
