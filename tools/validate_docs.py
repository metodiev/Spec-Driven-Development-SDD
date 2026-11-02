#!/usr/bin/env python3
"""Validate the SDD handbook.

Checks performed
----------------
1. Code fences are balanced and every opening fence has a language tag.
2. Relative Markdown links resolve to an existing file or directory.
3. In-page anchors (#fragment) and cross-file anchors exist.
4. Fenced ``json`` blocks parse as JSON.
5. Fenced ``yaml`` blocks and leading ``---`` front matter pass structural checks
   (full parse when PyYAML is installed).
6. Mermaid blocks start with a known diagram type and are structurally balanced.

Usage
-----
    python3 tools/validate_docs.py [--root .] [--json]

Exit code is 1 when any error is found. Warnings never fail the build unless
``--strict`` is passed.

Limitations
-----------
* External URLs are not fetched (offline-safe by design).
* YAML validation is structural unless PyYAML is importable.
* Mermaid is checked for structure, not rendered. Use the Mermaid CLI for a full
  render check when available.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:  # optional; the validator must work without third-party packages
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None


MERMAID_TYPES = {
    "flowchart",
    "graph",
    "sequencediagram",
    "statediagram",
    "statediagram-v2",
    "classdiagram",
    "erdiagram",
    "gitgraph",
    "journey",
    "timeline",
    "mindmap",
    "quadrantchart",
    "pie",
    "gantt",
    "c4context",
    "c4container",
    "block-beta",
    "sankey-beta",
    "xychart-beta",
    "requirementdiagram",
}

EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "target",
    "coverage",
    "__pycache__",
}


def iter_markdown(root: Path):
    """Yield Markdown files under root, skipping vendor and build directories."""
    for path in sorted(root.rglob("*.md")):
        if any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts[:-1]):
            continue
        yield path


FENCE_RE = re.compile(r"^(?P<fence>`{3,}|~{3,})(?P<info>[^`]*)$")
LINK_RE = re.compile(r"(?<!\!)\[(?P<text>[^\]]*)\]\((?P<target>[^)]+)\)")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


@dataclass
class Problem:
    path: str
    line: int
    kind: str
    message: str
    severity: str = "error"


@dataclass
class Report:
    files: int = 0
    fences: int = 0
    links: int = 0
    json_blocks: int = 0
    yaml_blocks: int = 0
    front_matter: int = 0
    mermaid_blocks: int = 0
    problems: list[Problem] = field(default_factory=list)

    def error(self, path: str, line: int, kind: str, message: str) -> None:
        self.problems.append(Problem(path, line, kind, message, "error"))

    def warn(self, path: str, line: int, kind: str, message: str) -> None:
        self.problems.append(Problem(path, line, kind, message, "warning"))

    @property
    def errors(self) -> list[Problem]:
        return [p for p in self.problems if p.severity == "error"]

    @property
    def warnings(self) -> list[Problem]:
        return [p for p in self.problems if p.severity == "warning"]


def slugify(text: str) -> str:
    """Approximate GitHub heading anchor generation."""
    text = text.strip().lower()
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return text


def collect_anchors(path: Path) -> set[str]:
    anchors: dict[str, int] = {}
    in_fence = False
    fence = ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        match = FENCE_RE.match(raw)
        if match:
            token = match.group("fence")
            if not in_fence:
                in_fence, fence = True, token
            elif token[0] == fence[0] and len(token) >= len(fence):
                in_fence = False
            continue
        if in_fence:
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", raw)
        if not heading:
            continue
        base = slugify(heading.group(2))
        seen = anchors.get(base, 0)
        anchors[base] = seen + 1
        yield_key = base if seen == 0 else f"{base}-{seen}"
        anchors[yield_key] = anchors.get(yield_key, 0) + 1
    return {key for key in anchors if anchors[key] > 0}


def check_links(path: Path, lines: list[str], report: Report, root: Path) -> None:
    in_fence = False
    fence = ""
    for number, raw in enumerate(lines, start=1):
        match = FENCE_RE.match(raw)
        if match:
            token = match.group("fence")
            if not in_fence:
                in_fence, fence = True, token
            elif token[0] == fence[0] and len(token) >= len(fence):
                in_fence = False
            continue
        if in_fence:
            continue

        # Inline code spans are examples, not links: `[text](url)` must not be
        # reported as a broken link.
        scannable = re.sub(r"`[^`]*`", "", raw)

        for link in LINK_RE.finditer(scannable):
            target = link.group("target").strip()
            if not target or target.startswith("mailto:"):
                continue
            if SCHEME_RE.match(target):
                continue

            report.links += 1

            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]

            file_part, _, anchor = target.partition("#")
            file_part = file_part.split("?", 1)[0]

            if not file_part:
                resolved = path
            else:
                resolved = (path.parent / file_part).resolve()

            if not resolved.exists():
                report.error(
                    str(path.relative_to(root)),
                    number,
                    "link",
                    f"missing target: {target}",
                )
                continue

            if anchor and resolved.is_file():
                anchors = collect_anchors(resolved)
                if anchor not in anchors:
                    report.error(
                        str(path.relative_to(root)),
                        number,
                        "anchor",
                        f"anchor '#{anchor}' not found in {resolved.name}",
                    )


def check_yaml_structure(text: str) -> list[str]:
    """Cheap structural checks that catch most hand-written YAML mistakes."""
    issues: list[str] = []
    in_block_scalar = False
    block_indent = None

    for number, raw in enumerate(text.splitlines(), start=1):
        if "\t" in raw:
            issues.append(f"line {number}: tab character in YAML")
            continue
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped in {"---", "..."}:
            continue

        if in_block_scalar:
            indent = len(raw) - len(raw.lstrip())
            if block_indent is None or indent > block_indent:
                continue
            in_block_scalar = False

        # block scalar start: "key: |" / "key: >" / "- |" etc.
        if re.search(r"(:|-)\s*[|>][+-]?\s*$", raw):
            in_block_scalar = True
            block_indent = len(raw) - len(raw.lstrip())
            continue

        quotes = stripped.count('"') - stripped.count('\\"')
        if quotes % 2:
            issues.append(f"line {number}: unbalanced double quotes")

        if stripped.startswith("-") or ":" in stripped:
            continue
        issues.append(f"line {number}: not a mapping or list entry: {stripped[:60]!r}")

    return issues


def check_tables(path: Path, lines: list[str], report: Report, root: Path) -> None:
    """Flag table rows whose column count differs from the header row.

    Escaped pipes (``\\|``) are ignored, which is the supported way to put a pipe
    inside a cell. An unescaped pipe inside inline code still splits the cell and is
    reported - that is intentional, because it silently breaks the rendered table.
    """
    rel = str(path.relative_to(root))
    in_fence = False
    fence = ""
    table: list[str] = []
    start = 0

    def columns(row: str) -> int:
        return row.replace("\\|", "").strip().strip("|").count("|") + 1

    def flush() -> None:
        nonlocal table
        if len(table) >= 2:
            expected = columns(table[0])
            for offset, row in enumerate(table[1:], start=1):
                core = row.strip().replace("|", "").replace(":", "").replace("-", "").replace(" ", "")
                if not core:
                    continue
                actual = columns(row)
                if actual != expected:
                    report.error(
                        rel,
                        start + offset,
                        "table",
                        f"row has {actual} columns but header has {expected}",
                    )
        table = []

    for number, raw in enumerate(lines, start=1):
        match = FENCE_RE.match(raw)
        if match:
            token = match.group("fence")
            if not in_fence:
                in_fence, fence = True, token
            elif token[0] == fence[0] and len(token) >= len(fence):
                in_fence = False
            flush()
            continue

        if in_fence:
            flush()
            continue

        if raw.strip().startswith("|"):
            if not table:
                start = number
            table.append(raw)
        else:
            flush()

    flush()


def check_mermaid(text: str) -> list[str]:
    issues: list[str] = []
    lines = [line for line in text.splitlines()]
    content = [line.strip() for line in lines if line.strip()]
    if not content:
        return ["empty Mermaid block"]

    header = content[0].split()[0].lower()
    if header not in MERMAID_TYPES:
        issues.append(f"unknown diagram type: {content[0][:60]!r}")

    if header in {"flowchart", "graph", "block-beta"}:
        opens = len(re.findall(r"^\s*subgraph\b", text, flags=re.M))
        closes = len(re.findall(r"^\s*end\s*$", text, flags=re.M))
        if opens != closes:
            issues.append(f"subgraph/end mismatch: {opens} subgraph vs {closes} end")

    for number, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("%%"):
            continue
        if stripped.count('"') % 2:
            issues.append(f"line {number}: unbalanced double quotes")

    return issues


def check_front_matter(text: str, rel: str, report: Report) -> None:
    """Validate a leading ``---`` YAML front-matter block, if present."""
    if not text.startswith("---\n"):
        return
    end = text.find("\n---\n", 3)
    if end == -1:
        report.error(rel, 1, "front-matter", "front matter opened but never closed with ---")
        return
    body = text[4 : end + 1]
    report.front_matter += 1
    if yaml is not None:
        try:
            data = yaml.safe_load(body)
        except Exception as exc:  # noqa: BLE001
            report.error(rel, 1, "front-matter", f"invalid YAML: {exc}")
            return
        if data is None:
            report.warn(rel, 1, "front-matter", "front matter block is empty")
        elif not isinstance(data, dict):
            report.error(rel, 1, "front-matter", "front matter is not a key/value mapping")
    else:
        for issue in check_yaml_structure(body):
            report.warn(rel, 1, "front-matter", issue)


def validate_file(path: Path, root: Path, report: Report) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    rel = str(path.relative_to(root))

    in_fence = False
    fence_token = ""
    info = ""
    buffer: list[str] = []
    start_line = 0

    check_front_matter(text, rel, report)

    for number, raw in enumerate(lines, start=1):
        match = FENCE_RE.match(raw)
        if match:
            token = match.group("fence")
            if not in_fence:
                in_fence = True
                fence_token = token
                info = match.group("info").strip().split()[0].lower() if match.group("info").strip() else ""
                buffer = []
                start_line = number
                report.fences += 1
                if not info:
                    report.warn(rel, number, "fence", "code fence without language tag")
                continue
            if token[0] == fence_token[0] and len(token) >= len(fence_token):
                in_fence = False
                body = "\n".join(buffer)
                if info == "json":
                    report.json_blocks += 1
                    try:
                        json.loads(body)
                    except json.JSONDecodeError as exc:
                        report.error(rel, start_line, "json", f"invalid JSON: {exc}")
                elif info in {"yaml", "yml"}:
                    report.yaml_blocks += 1
                    if yaml is not None:
                        try:
                            list(yaml.safe_load_all(body))
                        except Exception as exc:  # noqa: BLE001
                            report.error(rel, start_line, "yaml", f"invalid YAML: {exc}")
                    else:
                        for issue in check_yaml_structure(body):
                            report.warn(rel, start_line, "yaml", issue)
                elif info == "mermaid":
                    report.mermaid_blocks += 1
                    for issue in check_mermaid(body):
                        report.error(rel, start_line, "mermaid", issue)
                buffer = []
                info = ""
                continue

        if in_fence:
            buffer.append(raw)

    if in_fence:
        report.error(rel, start_line, "fence", "unclosed code fence")

    check_links(path, lines, report, root)
    check_tables(path, lines, report, root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the SDD handbook.")
    parser.add_argument("--root", default=".", help="documentation root (default: repository root)")
    parser.add_argument("--json", action="store_true", help="emit a JSON report")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: root not found: {root}", file=sys.stderr)
        return 2

    report = Report()
    for path in iter_markdown(root):
        report.files += 1
        validate_file(path, root, report)

    failures = report.errors + (report.warnings if args.strict else [])

    if args.json:
        payload = {
            "files": report.files,
            "fences": report.fences,
            "links": report.links,
            "json_blocks": report.json_blocks,
            "yaml_blocks": report.yaml_blocks,
            "front_matter": report.front_matter,
            "mermaid_blocks": report.mermaid_blocks,
            "errors": len(report.errors),
            "warnings": len(report.warnings),
            "problems": [
                {
                    "path": p.path,
                    "line": p.line,
                    "kind": p.kind,
                    "severity": p.severity,
                    "message": p.message,
                }
                for p in report.problems
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        for problem in report.problems:
            print(f"{problem.path}:{problem.line}: {problem.severity}: [{problem.kind}] {problem.message}")
        print()
        print(
            f"files={report.files} fences={report.fences} links={report.links} "
            f"json={report.json_blocks} yaml={report.yaml_blocks} "
            f"front_matter={report.front_matter} mermaid={report.mermaid_blocks}"
        )
        print(f"errors={len(report.errors)} warnings={len(report.warnings)}")
        if yaml is None:
            print("note: PyYAML not installed - YAML blocks were checked structurally only")
        if not report.problems:
            print("OK: no problems found")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
