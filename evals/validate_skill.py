#!/usr/bin/env python3
"""Static validator for the humanize-writing skill.

Checks structure, frontmatter, internal references, required content,
eval JSON shape, triggers, and acceptance-case plumbing. No third-party
dependencies. Exit code 0 on pass, 1 on failure.

Usage:
    python3 evals/validate_skill.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "references/ai-tells.md",
    "references/defensive-language.md",
    "references/examples.md",
    "references/style-profile.md",
]

REQUIRED_FILES = DOCS + [
    "evals/evals.json",
    "evals/triggers.json",
    "evals/acceptance/cases.json",
    "evals/acceptance/rubric.md",
    "evals/acceptance/README.md",
    "evals/acceptance/check_outputs.py",
    "evals/acceptance/stage_blind.py",
    "assets/example-style-profile.md",
]

DEFENSIVE_HEADINGS = [
    "## 1. Calibrated Caution vs Defensive Protection",
    "## 2. Marker Inventory",
    "## 3. Rewrite Strategies",
    "## 4. Genre Playbooks",
    "## 5. Boundaries",
    "## 6. Verification Checklist",
    "## 7. Focused Request Recipe",
]

CATEGORIES = [
    "### A. Meta-commentary",
    "### B. Assistant",
    "### C. Self-disqualification",
    "### D. Hedge stacking",
    "### E. Preemptive rebuttal",
    "### F. Reflexive limitation",
    "### G. Significance deflation",
    "### H. Narrative reader management",
    "### I. False balance",
    "### J. Liability boilerplate",
]

passes: list[str] = []
failures: list[tuple[str, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        passes.append(name)
    else:
        failures.append((name, detail))


def read(rel: str) -> str:
    return (REPO / rel).read_text(encoding="utf-8")


def main() -> int:
    # 1. Required files.
    for rel in REQUIRED_FILES:
        check(f"file exists: {rel}", (REPO / rel).is_file())

    missing = [rel for rel in REQUIRED_FILES if not (REPO / rel).is_file()]
    if missing:
        report()
        return 1

    # 2. SKILL.md frontmatter.
    skill = read("SKILL.md")
    fm = re.match(r"^---\n(.*?)\n---\n", skill, re.DOTALL)
    check("SKILL.md has YAML frontmatter", fm is not None)
    if fm:
        fields = {}
        for line in fm.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip().strip('"')
        check("frontmatter name is humanize-writing", fields.get("name") == "humanize-writing")
        check(
            "frontmatter description mentions defensive language",
            "defensive" in fields.get("description", "").lower(),
        )
        check("frontmatter version is 0.2.0", fields.get("version") == "0.2.0")

    for needle in [
        "## Defensive-Language Pass (Focused Mode)",
        "## Core Workflow",
        "## Key Rules",
        "## Resources",
        "Never add certainty",
        "Never strip required disclosures",
        "references/defensive-language.md",
        "not a compression pass",
        "new objects, dialogue, and plot events are invention",
    ]:
        check(f"SKILL.md contains: {needle}", needle in skill)

    # 3. Defensive-language reference.
    ref = read("references/defensive-language.md")
    for heading in DEFENSIVE_HEADINGS:
        check(f"defensive-language.md contains heading: {heading}", heading in ref)
    for category in CATEGORIES:
        check(f"defensive-language.md contains category: {category}", category in ref)
    for term in ["calibrated", "disclosures", "association", "causation", "checklist"]:
        check(f"defensive-language.md mentions: {term}", term.lower() in ref.lower())
    words = len(ref.split())
    check(f"defensive-language.md is substantive ({words} words >= 1200)", words >= 1200, f"{words} words")

    # 3b. Post-round fixes must be protected by the validator.
    check(
        "defensive-language.md contains the anti-compression rule",
        "Do not turn the pass into a compression pass" in ref,
    )
    check(
        "defensive-language.md contains the no-invention boundary",
        "Do not invent facts, citations, numbers, events, objects, or dialogue" in ref,
    )
    examples = read("references/examples.md")
    check(
        "examples.md warns against copying example details",
        "Never copy a name, gesture, object, or line of dialogue" in examples,
    )

    # 4. README.
    readme = read("README.md")
    for needle in [
        "defensive language",
        "references/defensive-language.md",
        "ACCEPTANCE.md",
        "validate_skill.py",
        "check_outputs.py",
    ]:
        check(f"README.md contains: {needle}", needle.lower() in readme.lower())

    # 5. CHANGELOG.
    changelog = read("CHANGELOG.md")
    check("CHANGELOG.md contains 0.2.0", "0.2.0" in changelog)
    check("CHANGELOG.md contains defensive language", "defensive" in changelog.lower())

    # 6. Evals.
    try:
        evals = json.loads(read("evals/evals.json"))
    except json.JSONDecodeError as exc:
        check("evals/evals.json parses", False, str(exc))
        evals = {}
    cases = evals.get("test_cases", [])
    check(f"evals has at least 8 cases (found {len(cases)})", len(cases) >= 8)
    names = {case.get("name", "") for case in cases}
    for expected in [
        "defensive_academic_cleanup",
        "defensive_calibrated_restraint",
        "defensive_narrative_cleanup",
        "defensive_email_cleanup",
    ]:
        check(f"evals contains case: {expected}", expected in names)
    for case in cases:
        label = case.get("name", "<unnamed>")
        check(f"eval case {label} has input", bool(case.get("input")))
        check(f"eval case {label} has >=2 assertions", len(case.get("assertions", [])) >= 2)

    try:
        triggers = json.loads(read("evals/triggers.json"))
    except json.JSONDecodeError as exc:
        check("evals/triggers.json parses", False, str(exc))
        triggers = {}
    trigger_cases = triggers.get("test_cases", [])
    positives = [t for t in trigger_cases if t.get("should_trigger") is True]
    negatives = [t for t in trigger_cases if t.get("should_trigger") is False]
    check(f"triggers has at least 10 positives (found {len(positives)})", len(positives) >= 10)
    check(f"triggers has at least 3 negatives (found {len(negatives)})", len(negatives) >= 3)
    check(
        "triggers include a Chinese defensive-language phrase",
        any("防御性语言" in t.get("input", "") for t in trigger_cases),
    )

    # 7. Internal references in SKILL.md and README.md resolve.
    for rel in ["SKILL.md", "README.md"]:
        text = read(rel)
        for match in re.finditer(r"`((?:references|evals|assets)/[^`\s]+)`", text):
            path = match.group(1)
            check(f"{rel} reference resolves: {path}", (REPO / path).exists())
        for match in re.finditer(r"\[[^\]]+\]\((?!https?://)([^)#]+)\)", text):
            path = match.group(1).strip()
            if path:
                check(f"{rel} markdown link resolves: {path}", (REPO / path).exists())

    # 8. Acceptance cases and inputs.
    try:
        accept = json.loads(read("evals/acceptance/cases.json"))
    except json.JSONDecodeError as exc:
        check("acceptance cases.json parses", False, str(exc))
        accept = {}
    accept_cases = accept.get("cases", [])
    check(f"acceptance has at least 4 cases (found {len(accept_cases)})", len(accept_cases) >= 4)
    ids = [case.get("id", "") for case in accept_cases]
    check("acceptance case ids are unique", len(ids) == len(set(ids)))
    for case in accept_cases:
        cid = case.get("id", "<unnamed>")
        check(f"acceptance case {cid} has prompt", bool(case.get("prompt")))
        check(f"acceptance case {cid} has genre", bool(case.get("genre")))
        check(f"acceptance case {cid} has input", bool(case.get("input")))
        checks = case.get("checks", {})
        check(f"acceptance case {cid} has defensive markers", len(checks.get("defensive_markers", [])) >= 1)
        check(f"acceptance case {cid} has must_keep", len(checks.get("must_keep", [])) >= 1)
        check(
            f"acceptance case {cid} has max_defensive_after",
            isinstance(checks.get("max_defensive_after"), int),
        )
        if "narrative" in case.get("genre", "").lower():
            low, high = checks.get("word_ratio", [0.0, 10.0])
            check(
                f"narrative case {cid} length bound is at least 0.67",
                low >= 0.67,
                f"found [{low}, {high}]",
            )
        input_path = REPO / "evals" / "acceptance" / "inputs" / f"{cid}.md"
        check(f"acceptance input file exists: {cid}.md", input_path.is_file())
        if input_path.is_file():
            check(
                f"acceptance input file matches case input: {cid}",
                case.get("input", "") in input_path.read_text(encoding="utf-8"),
            )

    # 8b. Anti-target-fitting: acceptance drafts must not appear in the skill
    # docs or the general eval file.
    def normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip().lower()

    corpus = normalize(
        "\n".join(
            read(rel)
            for rel in [
                "SKILL.md",
                "references/defensive-language.md",
                "references/ai-tells.md",
                "references/examples.md",
                "references/style-profile.md",
                "evals/evals.json",
            ]
        )
    )
    seen_inputs: set[str] = set()
    for case in accept_cases:
        cid = case.get("id", "<unnamed>")
        draft = normalize(case.get("input", ""))
        check(f"acceptance draft {cid} does not appear in skill docs or evals", draft not in corpus)
        check(f"acceptance draft {cid} is unique", draft not in seen_inputs)
        seen_inputs.add(draft)

    acceptance_readme = read("evals/acceptance/README.md")
    for needle in ["unseen", "blind", "stage_blind.py", "70–115%"]:
        check(f"acceptance README contains: {needle}", needle.lower() in acceptance_readme.lower())

    # 9. No placeholders in docs.
    for rel in DOCS:
        text = read(rel)
        for placeholder in ["TODO", "FIXME", "lorem ipsum", "TBD"]:
            check(f"{rel} has no placeholder: {placeholder}", placeholder.lower() not in text.lower())

    # 10. Eval scripts compile.
    for rel in [
        "evals/validate_skill.py",
        "evals/acceptance/check_outputs.py",
        "evals/acceptance/stage_blind.py",
    ]:
        try:
            compile(read(rel), rel, "exec")
            check(f"{rel} compiles", True)
        except SyntaxError as exc:
            check(f"{rel} compiles", False, str(exc))

    report()
    return 1 if failures else 0


def report() -> None:
    print(f"Static validation: {len(passes)} passed, {len(failures)} failed\n")
    if failures:
        print("FAILED CHECKS")
        for name, detail in failures:
            print(f"  FAIL  {name}" + (f" — {detail}" if detail else ""))
        print()
    print("RESULT: " + ("FAIL" if failures else "PASS"))


if __name__ == "__main__":
    sys.exit(main())
