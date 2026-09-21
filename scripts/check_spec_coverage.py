"""Report drift between swagger.yaml and threecx/services/.

Usage:
    python scripts/check_spec_coverage.py          # human-readable report
    python scripts/check_spec_coverage.py --quiet  # only the summary line

Exits non-zero when the SDK and the spec disagree, so it doubles as a CI gate
(see tests/test_spec_coverage.py).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from spec_tools import drift, spec_operations  # noqa: E402


def main() -> int:
    quiet = "--quiet" in sys.argv
    ops = spec_operations()
    missing, stale = drift()
    covered = len(ops) - len(missing)

    print(f"spec paths: {len(ops)} | covered: {covered} | missing: {len(missing)} | stale: {len(stale)}")

    if not quiet and missing:
        by_tag: dict[str, list[str]] = {}
        for path, entries in missing.items():
            for method, op_id, tag in entries:
                by_tag.setdefault(tag, []).append(f"{method:6} {path}  ({op_id})")
        total = sum(len(v) for v in by_tag.values())
        print(f"\n### In the spec, not in the SDK ({total} operations)")
        for tag in sorted(by_tag):
            print(f"\n-- {tag} [{len(by_tag[tag])}]")
            for line in sorted(by_tag[tag]):
                print("   ", line)

    if not quiet and stale:
        print(f"\n### Called by the SDK, not in the spec ({len(stale)})")
        for url in sorted(stale):
            print("   ", url, sorted(stale[url]))

    if missing or stale:
        print("\nDrift detected. Update threecx/services/ (or KNOWN_INLINED in scripts/spec_tools.py).")
        return 1

    print("No drift: every spec operation has a service method and vice versa.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
