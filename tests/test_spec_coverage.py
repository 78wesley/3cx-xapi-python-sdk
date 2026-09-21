"""Fail the suite when swagger.yaml and threecx/services/ drift apart.

swagger.yaml is committed, so a new spec shows up as a diff and these tests say
exactly what the service layer still owes it. See CLAUDE.md, "Updating to a new
swagger.yaml".
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

pytest.importorskip("yaml", reason="pyyaml is needed for spec-drift checks (pip install -e '.[dev]')")

# scripts/ and swagger.yaml are excluded from the sdist, so these checks only
# apply in a git checkout. Missing scripts/ means "not a checkout" -> skip;
# a checkout with scripts/ but no swagger.yaml still fails loudly below.
spec_tools = pytest.importorskip(
    "spec_tools", reason="scripts/ is not shipped in the sdist; spec-drift checks run in the repo only"
)

SPEC = spec_tools.SPEC
drift = spec_tools.drift
spec_operations = spec_tools.spec_operations


def _format(lines: list[str], header: str) -> str:
    return "\n".join([header, *lines, ""])


def test_swagger_is_present() -> None:
    assert SPEC.exists(), "swagger.yaml is the source of truth and must stay committed"


def test_every_spec_operation_has_a_service_method() -> None:
    missing, _ = drift()
    if missing:
        lines = [
            f"  {method:6} {path}  ({op_id})"
            for path, entries in sorted(missing.items())
            for method, op_id, _tag in entries
        ]
        pytest.fail(
            _format(
                lines,
                f"{len(lines)} operation(s) in swagger.yaml have no method in threecx/services/:",
            ),
            pytrace=False,
        )


def test_no_service_calls_a_route_the_spec_dropped() -> None:
    _, stale = drift()
    if stale:
        lines = [f"  {url}  <- {', '.join(sorted(files))}" for url, files in sorted(stale.items())]
        pytest.fail(
            _format(
                lines,
                f"{len(stale)} URL(s) built by threecx/services/ are absent from swagger.yaml:",
            ),
            pytrace=False,
        )


def test_spec_parses_to_a_sane_number_of_operations() -> None:
    # Guards against a truncated or half-downloaded swagger.yaml silently
    # turning both drift checks green.
    assert len(spec_operations()) > 400
