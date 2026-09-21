"""Shared helpers for comparing swagger.yaml against the hand-written services.

Imported by scripts/check_spec_coverage.py and tests/test_spec_coverage.py.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "swagger.yaml"
SERVICES = ROOT / "threecx" / "services"

HTTP_METHODS = ("get", "post", "patch", "delete", "put")

# Endpoints the SDK deliberately calls with some path parameters hard-coded,
# so the rendered URL cannot be matched back to the spec template by shape.
# Each entry must still correspond to a real spec path.
KNOWN_INLINED = {
    "/ReportCallLogData/Pbx.GetCallLogData": "reports.get_call_log pins the optional filters to their defaults",
}


def normalise(url: str) -> str:
    """Reduce a spec path or a rendered f-string to a comparable shape."""
    url = re.sub(r"\{[^{}]*\}", "{}", url)
    url = re.sub(r"'\{\}'", "{}", url)  # (Number='{}') -> (Number={})
    return url.rstrip("/")


def load_spec() -> Dict[str, Any]:
    if not SPEC.exists():
        raise FileNotFoundError(f"{SPEC} is missing - it is the source of truth for this SDK")
    return yaml.safe_load(SPEC.read_text())  # type: ignore[no-any-return]


def spec_operations() -> Dict[str, List[Tuple[str, str, str]]]:
    """Map normalised path -> [(METHOD, operationId, tag), ...]."""
    ops: Dict[str, List[Tuple[str, str, str]]] = {}
    for path, item in load_spec()["paths"].items():
        for method, op in item.items():
            if method not in HTTP_METHODS:
                continue
            tag = (op.get("tags") or ["?"])[0]
            ops.setdefault(normalise(path), []).append((method.upper(), op.get("operationId", "?"), tag))
    return ops


class _UrlCollector(ast.NodeVisitor):
    """Collect URL literals, resolving `{self._PATH}`-style class constants."""

    def __init__(self, consts: Dict[str, str]) -> None:
        self.consts = consts
        self.urls: Set[str] = set()

    def _render(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.JoinedStr):
            out = ""
            for part in node.values:
                if isinstance(part, ast.Constant):
                    out += str(part.value)
                elif isinstance(part, ast.FormattedValue) and isinstance(part.value, ast.Attribute):
                    out += self.consts.get(part.value.attr, "{}")
                else:
                    out += "{}"
            return out
        return None

    def generic_visit(self, node: ast.AST) -> None:
        rendered = self._render(node)
        if rendered and rendered.startswith("/"):
            self.urls.add(rendered)
            if isinstance(node, ast.JoinedStr):
                # Do not descend: the literal chunks of an f-string are fragments,
                # not URLs in their own right.
                return
        super().generic_visit(node)


def service_urls() -> Dict[str, Set[str]]:
    """Map normalised URL -> {service module names that build it}."""
    found: Dict[str, Set[str]] = {}
    for file in sorted(SERVICES.glob("*.py")):
        tree = ast.parse(file.read_text())
        consts = {
            node.targets[0].id: node.value.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        }
        collector = _UrlCollector(consts)
        collector.visit(tree)
        for url in collector.urls:
            found.setdefault(normalise(url), set()).add(file.name)
    return found


def drift() -> Tuple[Dict[str, List[Tuple[str, str, str]]], Dict[str, Set[str]]]:
    """Return (spec operations with no service method, service URLs absent from the spec)."""
    ops = spec_operations()
    urls = service_urls()

    missing = {path: meta for path, meta in ops.items() if path not in urls}
    stale = {
        url: files
        for url, files in urls.items()
        if url not in ops and not any(url.startswith(prefix) for prefix in KNOWN_INLINED)
    }
    return missing, stale
