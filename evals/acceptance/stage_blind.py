#!/usr/bin/env python3
"""Stage a blind copy of the skill for behavioral acceptance.

The blind copy contains only the files a normal skill user would load:
SKILL.md, the reference docs, the example profile, and the acceptance inputs.
It deliberately excludes:

  - evals/ (contains test drafts, assertions, and scoring code)
  - references/examples.md (contains worked "after" answers)

This keeps the rewriter from seeing the test cases, assertions, and scoring
code. The staged reference still contains its generic worked examples in
section 4, so this is blind to the test set rather than strictly answer-key-free. The script also records
SHA-256 hashes of the case file and staged skill files so the run can be
audited and reproduced.

Usage:
    python3 evals/acceptance/stage_blind.py --out <directory>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ACCEPT = REPO / "evals" / "acceptance"

SKILL_FILES = [
    "SKILL.md",
    "references/defensive-language.md",
    "references/ai-tells.md",
    "references/style-profile.md",
    "assets/example-style-profile.md",
]

BLIND_NOTE = """# Blind Acceptance Copy

This directory is a deliberately reduced copy of the humanize-writing skill for
behavioral acceptance. `evals/` and `references/examples.md` are absent on
purpose: they contain test drafts, assertions, and worked answers.

Rules for the rewriter:
- Read `SKILL.md` and `references/defensive-language.md` first.
- If `SKILL.md` points to `references/examples.md`, treat it as unavailable.
- Do not look outside this directory.
- For each file in `inputs/`, write only the final rewritten text to
  `outputs/<case-id>.md` (no preamble, headings, code fences, or change logs).
"""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, help="target directory for the blind copy")
    args = parser.parse_args()
    out = Path(args.out).resolve()
    if out.exists():
        shutil.rmtree(out)
    (out / "references").mkdir(parents=True)
    (out / "assets").mkdir(parents=True)
    (out / "inputs").mkdir(parents=True)
    (out / "outputs").mkdir(parents=True)

    manifest = {
        "cases_sha256": sha256(ACCEPT / "cases.json"),
        "files": {},
        "inputs": {},
        "blind_test_sha256": None,
    }
    for rel in SKILL_FILES:
        src = REPO / rel
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        manifest["files"][rel] = sha256(src)

    for src in sorted((ACCEPT / "inputs").glob("*.md")):
        shutil.copy2(src, out / "inputs" / src.name)
        manifest["inputs"][src.name] = sha256(src)

    (out / "BLIND_TEST.md").write_text(BLIND_NOTE, encoding="utf-8")
    manifest["blind_test_sha256"] = hashlib.sha256((out / "BLIND_TEST.md").read_bytes()).hexdigest()
    (out / "blind_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Blind copy staged at: {out}")
    print(f"cases_sha256: {manifest['cases_sha256']}")
    for rel, digest in manifest["files"].items():
        print(f"  {digest[:16]}  {rel}")
    for name, digest in manifest["inputs"].items():
        print(f"  {digest[:16]}  inputs/{name}")
    print(f"  {manifest['blind_test_sha256'][:16]}  BLIND_TEST.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
