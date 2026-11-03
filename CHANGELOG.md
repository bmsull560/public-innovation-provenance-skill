# Changelog

## 1.1

- Trigger evals and behavioral evals for grant, patent, SBIR, product-page, and verdict prompts.
- Golden pack and should-fail packs. `scripts/test-checker.py` runs them.
- Checker requires `generated_at`, ISO dates, the edge-type list, and non-empty `SOURCES.md`.
- Institution and company seeds must be node type `organization`. A `company` node fails.
- Unresolved hops use `search:<system>` plus a `gaps[]` hop of `from|type|to`. Other empty identifiers fail.
- Banned judgment phrases are scanned in the JSON as well as the report. Non-object ledger rows fail cleanly.
- Report stub uses `person` and `license`, not an `inventor` node.

## 1.0

- Initial skill: forward and reverse provenance, public-return ledger, pack checker.
