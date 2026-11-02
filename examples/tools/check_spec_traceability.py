#!/usr/bin/env python3
"""Example CI check: every acceptance criterion is referenced in the PR description.

This checks *reference*, not correctness. Correctness is established by the
verification report and independent review. See docs/25-ci-cd-integration.md.

Usage:
    python3 check_spec_traceability.py <spec.md> <pr-body.md> [--json]

Exit codes:
    0  every AC is referenced
    1  at least one AC is missing
    2  usage or file error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AC_RE = re.compile(r"\bAC-\d+\.\d+\b")


def load(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        raise SystemExit(2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", help="path to spec.md")
    parser.add_argument("pr_body", help="path to the PR description")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    spec = load(args.spec)
    body = load(args.pr_body)

    required = sorted(set(AC_RE.findall(spec)), key=lambda a: tuple(map(int, a[3:].split("."))))
    missing = [ac for ac in required if ac not in body]

    if args.json:
        print(json.dumps({"required": required, "missing": missing}, indent=2))
    else:
        print(f"spec={args.spec} acceptance_criteria={len(required)}")
        if missing:
            print("missing from PR description:")
            for ac in missing:
                print(f"  - {ac}")
        else:
            print("all acceptance criteria referenced")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
