#!/usr/bin/env python3
"""Validate a public-innovation-provenance pack directory."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_FILES = ("PROVENANCE.md", "provenance.json", "GAPS.md", "SOURCES.md")
NODE_TYPES = {
    "grant",
    "recipient",
    "subrecipient",
    "person",
    "publication",
    "invention",
    "patent",
    "assignment",
    "license",
    "organization",
    "product",
    "capital_event",
    "acquisition",
    "procurement",
}
CONFIDENCE = {
    "established",
    "corroborated",
    "inferred",
    "unresolved",
    "not-applicable",
}
EDGE_REQUIRED = ("from", "type", "to", "confidence", "source", "identifier", "as_of")
RETURN_DIMENSIONS = (
    "Public funding",
    "Research output",
    "IP",
    "Ownership",
    "Government license",
    "Licensing",
    "Commercialization",
    "Capitalization",
    "Acquisition",
    "Government use",
    "Public access",
    "Revenue",
    "Royalty",
    "Follow-on public funding",
)
BANNED_PHRASES = (
    "taxpayer roi",
    "bang-for-buck",
    "taxpayers funded it and",
    "improper privatization",
    "the government got nothing",
)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing {path.name}")
    except json.JSONDecodeError as exc:
        fail(f"{path.name} is not valid JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.name} root must be an object")
    return data


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: check-provenance.py <pack-dir>")
    pack = Path(sys.argv[1])
    if not pack.is_dir():
        fail(f"not a directory: {pack}")

    for name in REQUIRED_FILES:
        if not (pack / name).is_file():
            fail(f"missing {name}")

    data = load_json(pack / "provenance.json")
    if data.get("schema") != "public-innovation-provenance.v1":
        fail("schema must be public-innovation-provenance.v1")

    seed = data.get("seed") or {}
    if not seed.get("type") or not seed.get("id"):
        fail("seed.type and seed.id are required")

    direction = data.get("direction")
    if not isinstance(direction, list) or not direction:
        fail("direction must be a non-empty list of forward and/or reverse")
    for item in direction:
        if item not in {"forward", "reverse"}:
            fail(f"unknown direction {item!r}")

    nodes = data.get("nodes")
    edges = data.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        fail("nodes and edges must be lists")
    if not nodes:
        fail("nodes must contain the seed entity at minimum")

    ids = []
    for node in nodes:
        if not isinstance(node, dict) or "id" not in node or "type" not in node:
            fail("every node needs id and type")
        if node["type"] not in NODE_TYPES:
            fail(f"unknown node type {node['type']!r}")
        if node["id"] in ids:
            fail(f"duplicate node id {node['id']!r}")
        ids.append(node["id"])
    idset = set(ids)
    if seed["id"] not in idset:
        fail(f"seed id {seed['id']!r} is not in nodes")

    for edge in edges:
        if not isinstance(edge, dict):
            fail("edges must be objects")
        for key in EDGE_REQUIRED:
            if not str(edge.get(key) or "").strip():
                fail(f"edge missing {key}")
        if edge["confidence"] not in CONFIDENCE:
            fail(f"bad edge confidence {edge['confidence']!r}")
        if edge["from"] not in idset or edge["to"] not in idset:
            fail(f"edge {edge['from']} -> {edge['to']} references missing node")

    returns = data.get("public_return")
    if not isinstance(returns, list) or len(returns) < 14:
        fail("public_return must list all 14 dimensions")
    seen = [row.get("dimension") for row in returns if isinstance(row, dict)]
    for dim in RETURN_DIMENSIONS:
        if dim not in seen:
            fail(f"public_return missing dimension {dim!r}")
    for row in returns:
        if row.get("confidence") not in CONFIDENCE:
            fail(f"bad public_return confidence on {row.get('dimension')!r}")
        if not str(row.get("finding") or "").strip():
            fail(f"empty finding on {row.get('dimension')!r}")

    gaps = data.get("gaps")
    if not isinstance(gaps, list):
        fail("gaps must be a list")
    for gap in gaps:
        if not isinstance(gap, dict):
            fail("gap entries must be objects")
        for key in ("hop", "searched", "would_close"):
            if not str(gap.get(key) or "").strip():
                fail(f"gap missing {key}")

    blob = "\n".join(
        (pack / name).read_text(encoding="utf-8", errors="ignore").lower()
        for name in ("PROVENANCE.md", "GAPS.md")
    )
    for phrase in BANNED_PHRASES:
        if phrase in blob:
            fail(f"report contains banned judgment phrase {phrase!r}")

    placeholders = ("{{seed_label}}", "{{generated_at}}", "{{direction}}")
    report = (pack / "PROVENANCE.md").read_text(encoding="utf-8", errors="ignore")
    for token in placeholders:
        if token in report:
            fail(f"PROVENANCE.md still has template token {token}")

    print(f"OK: {pack} nodes={len(nodes)} edges={len(edges)} gaps={len(gaps)}")


if __name__ == "__main__":
    main()
