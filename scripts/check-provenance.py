#!/usr/bin/env python3
"""Validate a public-innovation-provenance pack directory."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
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
# Institution and company are seed classes. The node is always an organization.
SEED_NODE = {
    "grant": "grant",
    "publication": "publication",
    "invention": "invention",
    "patent": "patent",
    "institution": "organization",
    "company": "organization",
    "product": "product",
    "person": "person",
}
EDGE_TYPES = {
    "funds",
    "subawards",
    "employs_or_appoints",
    "acknowledges",
    "authors",
    "invents",
    "discloses",
    "matures_to",
    "continuation_of",
    "cites",
    "owned_by",
    "assigned_by",
    "assigned_to",
    "government_interest",
    "licenses",
    "options",
    "spins_out",
    "embodies",
    "sells",
    "procures",
    "acquires",
    "invests",
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
SCAN_FILES = ("PROVENANCE.md", "GAPS.md", "SOURCES.md", "provenance.json")
PLACEHOLDERS = ("{{seed_label}}", "{{generated_at}}", "{{direction}}")
SEARCH_ID = re.compile(r"search:[a-z0-9][a-z0-9+._-]{0,63}\Z")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def valid_iso(value: object) -> bool:
    if not isinstance(value, str) or len(value) != 10:
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


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


def hop_key(edge: dict) -> str:
    return f"{edge['from']}|{edge['type']}|{edge['to']}"


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
    if not valid_iso(data.get("generated_at")):
        fail("generated_at must be YYYY-MM-DD")

    seed = data.get("seed") or {}
    if not isinstance(seed, dict) or not seed.get("type") or not seed.get("id"):
        fail("seed.type and seed.id are required")
    if seed["type"] not in SEED_NODE:
        fail(f"unknown seed type {seed['type']!r}")
    if len(str(seed["id"])) < 3:
        fail("seed.id must be at least 3 characters")

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
    by_id = {}
    for node in nodes:
        if not isinstance(node, dict) or "id" not in node or "type" not in node:
            fail("every node needs id and type")
        if node["type"] not in NODE_TYPES:
            fail(f"unknown node type {node['type']!r}")
        if node["id"] in by_id:
            fail(f"duplicate node id {node['id']!r}")
        ids.append(node["id"])
        by_id[node["id"]] = node
    if seed["id"] not in by_id:
        fail(f"seed id {seed['id']!r} is not in nodes")
    expected = SEED_NODE[seed["type"]]
    actual = by_id[seed["id"]]["type"]
    if actual != expected:
        fail(f"seed type {seed['type']} requires node type {expected}, found {actual}")

    gaps = data.get("gaps")
    if not isinstance(gaps, list):
        fail("gaps must be a list")
    gap_hops = set()
    for gap in gaps:
        if not isinstance(gap, dict):
            fail("gap entries must be objects")
        for key in ("hop", "searched", "would_close"):
            if not str(gap.get(key) or "").strip():
                fail(f"gap missing {key}")
        gap_hops.add(gap["hop"])

    idset = set(ids)
    for edge in edges:
        if not isinstance(edge, dict):
            fail("edges must be objects")
        for key in EDGE_REQUIRED:
            if not str(edge.get(key) or "").strip():
                fail(f"edge missing {key}")
        if edge["type"] not in EDGE_TYPES:
            fail(f"unknown edge type {edge['type']!r}")
        if edge["confidence"] not in CONFIDENCE:
            fail(f"bad edge confidence {edge['confidence']!r}")
        if not valid_iso(edge.get("as_of")):
            fail(f"edge {hop_key(edge)} as_of must be YYYY-MM-DD")
        if edge["from"] not in idset or edge["to"] not in idset:
            fail(f"edge {edge['from']} -> {edge['to']} references missing node")
        ident = str(edge["identifier"]).strip()
        hop = hop_key(edge)
        if ident.startswith("search:"):
            if edge["confidence"] != "unresolved":
                fail(f"search: identifiers are only valid on unresolved edges ({hop})")
            if SEARCH_ID.fullmatch(ident) is None:
                fail(f"unresolved edge {hop} identifier must match search:<system>")
        if edge["confidence"] == "unresolved" and hop not in gap_hops:
            fail(f"unresolved edge {hop} has no matching gap")

    returns = data.get("public_return")
    if not isinstance(returns, list) or len(returns) < 14:
        fail("public_return must list all 14 dimensions")
    seen = []
    for row in returns:
        if not isinstance(row, dict):
            fail("public_return entries must be objects")
        seen.append(row.get("dimension"))
        if row.get("confidence") not in CONFIDENCE:
            fail(f"bad public_return confidence on {row.get('dimension')!r}")
        if not str(row.get("finding") or "").strip():
            fail(f"empty finding on {row.get('dimension')!r}")
    for dim in RETURN_DIMENSIONS:
        if dim not in seen:
            fail(f"public_return missing dimension {dim!r}")

    blob = "\n".join(
        (pack / name).read_text(encoding="utf-8", errors="ignore").lower()
        for name in SCAN_FILES
    )
    for phrase in BANNED_PHRASES:
        if phrase in blob:
            fail(f"report contains banned judgment phrase {phrase!r}")

    report = (pack / "PROVENANCE.md").read_text(encoding="utf-8", errors="ignore")
    for token in PLACEHOLDERS:
        if token in report:
            fail(f"PROVENANCE.md still has template token {token}")

    sources = (pack / "SOURCES.md").read_text(encoding="utf-8", errors="ignore")
    if not sources.strip():
        fail("SOURCES.md is empty")

    print(f"OK: {pack} nodes={len(nodes)} edges={len(edges)} gaps={len(gaps)}")


if __name__ == "__main__":
    main()
