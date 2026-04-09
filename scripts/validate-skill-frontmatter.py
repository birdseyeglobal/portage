#!/usr/bin/env python3
"""Validate SKILL.md YAML frontmatter against the Claude Code skill spec.

Allowed fields (strict):
  - name        (required)
  - description (required)

Any other top-level field is an error. The `name` field must match the
skill's directory name.

Extend ALLOWED_FIELDS below on a case-by-case basis if a non-standard
field is deliberately adopted.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ALLOWED_FIELDS = frozenset({"name", "description"})
REQUIRED_FIELDS = frozenset({"name", "description"})

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def top_level_keys(frontmatter: str) -> list[tuple[str, str]]:
    """Return a list of (key, value) pairs for top-level YAML keys.

    Handles simple `key: value` and block scalars (`key: |` / `key: >`)
    by consuming the indented continuation lines. Nested mappings are
    skipped for the value but the top-level key is still captured.
    """
    pairs: list[tuple[str, str]] = []
    lines = frontmatter.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # A top-level key is a line that starts in column 0 and contains ':'.
        if line and not line[0].isspace() and ":" in line:
            key, _, rest = line.partition(":")
            key = key.strip()
            value = rest.strip()
            # If value is a block scalar marker, consume continuation.
            if value in {"|", ">", "|-", ">-", "|+", ">+"}:
                collected: list[str] = []
                i += 1
                while i < len(lines) and (lines[i] == "" or lines[i][:1].isspace()):
                    collected.append(lines[i].lstrip())
                    i += 1
                value = " ".join(s for s in collected if s).strip()
                pairs.append((key, value))
                continue
            pairs.append((key, value))
        i += 1
    return pairs


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    match = FRONTMATTER_RE.match(text)
    if not match:
        return [f"{path}: missing or malformed YAML frontmatter"]

    pairs = top_level_keys(match.group(1))
    keys = {k for k, _ in pairs}
    values = dict(pairs)

    for field in sorted(REQUIRED_FIELDS - keys):
        errors.append(f"{path}: missing required field '{field}'")

    for field in sorted(keys - ALLOWED_FIELDS):
        errors.append(
            f"{path}: non-standard field '{field}' "
            f"(allowed: {sorted(ALLOWED_FIELDS)})"
        )

    if "name" in values:
        name = values["name"].strip().strip('"').strip("'")
        dir_name = path.parent.name
        if name != dir_name:
            errors.append(
                f"{path}: frontmatter name '{name}' does not match "
                f"directory '{dir_name}'"
            )

    if "description" in values:
        description = values["description"].strip().strip('"').strip("'")
        if not description:
            errors.append(f"{path}: description is empty")

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    skills = sorted(repo_root.glob("plugins/*/skills/*/SKILL.md"))

    if not skills:
        print("No SKILL.md files found under plugins/*/skills/*/", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for skill in skills:
        all_errors.extend(validate(skill))

    if all_errors:
        for err in all_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(
            f"\n{len(all_errors)} error(s) across {len(skills)} skill(s)",
            file=sys.stderr,
        )
        return 1

    print(f"OK: {len(skills)} skill(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
