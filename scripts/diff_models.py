"""Summarise what a model regeneration changed.

`git diff threecx/models/_generated.py` shows every line; this shows the shape:
which classes appeared, vanished, and which fields moved or changed type. Use it
after `python scripts/generate_models.py` to spot breaking changes.

Usage:
    python scripts/diff_models.py              # committed HEAD vs working tree
    python scripts/diff_models.py <ref>        # <ref> vs working tree
"""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path
from typing import Dict, Tuple

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "threecx" / "models" / "_generated.py"
REL = TARGET.relative_to(ROOT).as_posix()

Model = Dict[str, Tuple[Dict[str, str], list[str]]]


def parse(source: str) -> Model:
    models: Model = {}
    for node in ast.parse(source).body:
        if not isinstance(node, ast.ClassDef):
            continue
        fields: Dict[str, str] = {}
        for stmt in node.body:
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                fields[stmt.target.id] = ast.unparse(stmt.annotation)
            elif (
                isinstance(stmt, ast.Assign)
                and len(stmt.targets) == 1
                and isinstance(stmt.targets[0], ast.Name)
            ):
                fields[stmt.targets[0].id] = ast.unparse(stmt.value)[:60]
        models[node.name] = (fields, [ast.unparse(b) for b in node.bases])
    return models


def main() -> int:
    ref = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    try:
        before = subprocess.run(
            ["git", "show", f"{ref}:{REL}"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except subprocess.CalledProcessError:
        print(f"Cannot read {REL} at {ref} - is it committed yet?")
        return 1

    old, new = parse(before), parse(TARGET.read_text())
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))

    print(f"classes: {len(old)} ({ref}) -> {len(new)} (working tree)")

    if added:
        print(f"\n### New ({len(added)})")
        for name in added:
            print(f"  + {name}")
    if removed:
        print(f"\n### Removed ({len(removed)})  <-- breaking for anyone importing these")
        for name in removed:
            print(f"  - {name}")

    changed = 0
    lines: list[str] = []
    for name in sorted(set(old) & set(new)):
        old_fields, old_bases = old[name]
        new_fields, new_bases = new[name]
        gained = sorted(set(new_fields) - set(old_fields))
        lost = sorted(set(old_fields) - set(new_fields))
        retyped = sorted(k for k in set(old_fields) & set(new_fields) if old_fields[k] != new_fields[k])
        if not (gained or lost or retyped or old_bases != new_bases):
            continue
        changed += 1
        lines.append(f"\n  ~ {name}")
        if old_bases != new_bases:
            lines.append(f"      base: {old_bases} -> {new_bases}")
        for k in gained:
            lines.append(f"      + {k}: {new_fields[k]}")
        for k in lost:
            lines.append(f"      - {k}: {old_fields[k]}")
        for k in retyped:
            lines.append(f"      ~ {k}: {old_fields[k]}  ->  {new_fields[k]}")

    if changed:
        print(f"\n### Changed ({changed})")
        print("\n".join(lines))

    if not (added or removed or changed):
        print("\nNo model changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
