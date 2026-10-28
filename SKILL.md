---
name: public-innovation-provenance
description: >-
  Reconstruct the lifecycle of publicly funded research from grant to IP
  to ownership to license to company to product, or run the chain
  backwards from a patent, company, or product. Use when auditing
  grant-to-commercialization provenance, Bayh-Dole ownership, university
  tech transfer, spinouts, public-return accounting, patent
  government-interest statements, FAIN or award traces, or joining a
  funding graph to a knowledge/IP graph. Not for taxpayer ROI, price
  targets, trade ideas, complaint drafts, or a verdict that a deal was
  good or bad.
metadata:
  type: workflow
  version: "1.1"
  domain: public-innovation-provenance
---

# Public Innovation Provenance

Trace public money into knowledge, property, and markets. Every arrow is an evidence problem. Commercialization is not a verdict.

## Enemy

A story that says public funding became a private product without a source, identifier, date, and confidence on each hop.

## One rule

No hop is established unless it carries `source`, a real record `identifier`, `as_of`, and `confidence`. When the record is not public, set `confidence` to `unresolved`, set `identifier` to `search:<system>` (for example `search:edgar`), and add a `gaps[]` row whose `hop` is `from|type|to`. Any other missing identifier fails the pack. Do not invent grant numbers, assignment dates, exclusive licenses, royalty streams, or "the government got nothing."

## Question

Forward — given a grant, what happened to the funded knowledge after the award ended?

Reverse — given a patent, company, product, or person, did publicly funded research contribute, and through which hops?

## Seed

Accept exactly one primary seed, plus optional secondary seeds. Classify it before searching.

| Seed | Id shape | First hop |
|---|---|---|
| Grant / award | agency award id, FAIN, NIH activity+serial | recipient, PIs, publications, reported inventions |
| Publication | DOI, PMID, PMCID | acknowledged grants, authors as inventors |
| Invention / patent | application, publication, or patent number | inventors, assignees, government interest, assignments, licenses |
| Institution | UEI, DUNS legacy, EIN, ROR | awards, TTO, spinouts |
| Company | legal name + jurisdiction, CIK, UEI | licenses in, assignments, products, procurement, capital |
| Product | trade name + regulatory id | patents, labels, procurement, owner |
| Person | legal name plus affiliation or ORCID | publications and patents, then those seeds |

Institution and company seeds are stored as node type `organization`. `seed.type` stays `institution` or `company`. A person seed is not walked until that identity is resolved.

If the seed is ambiguous, resolve identity first. Do not start two graphs and merge them later by similar names.

## Workflow

Execute in order. Do not skip gap recording.

1. Resolve identity of the seed. Write the canonical id and aliases.
2. Walk **Grant → Research** using [references/sources.md](references/sources.md). Capture award fields in [references/graph-schema.md](references/graph-schema.md).
3. Walk **Research → IP**. Prefer independent cross-links (grant number on paper, inventor on patent, government-interest clause naming the award).
4. Walk **IP → Ownership**. Assignment chain beats website copy. Bayh-Dole defaults live in [references/ownership.md](references/ownership.md).
5. Walk **IP → Commercialization**. License, option, spinout, product, clearance, procurement, capital, acquisition.
6. If the user seeded a patent, company, product, or person, also run [references/reverse-traversal.md](references/reverse-traversal.md).
7. Fill the public-return ledger in [references/public-return.md](references/public-return.md). Accounting only. No "good deal / bad deal."
8. Emit the pack from [assets/provenance-report.md](assets/provenance-report.md) plus `artifacts/<slug>/provenance.json` matching [assets/provenance.schema.json](assets/provenance.schema.json).
9. Run `scripts/check-provenance.py <pack-dir>` before calling the pack done.

Join to a fund-flow graph only at shared nodes (`grant`, `recipient`, `subrecipient`, `contractor`). Do not collapse money hops into IP hops.

Density bar — [references/worked-example.md](references/worked-example.md).

## Confidence

Use only these labels on edges and on public-return cells.

| Label | Meaning |
|---|---|
| established | Primary record with a stable identifier (award API, patent grant, recorded assignment, labeled FDA application) |
| corroborated | Two independent public sources agree on the same hop |
| inferred | One weak source or name match only. Must state the alternative |
| unresolved | Searched, not found, or access-walled (license text, iEdison invention report, royalty ledger) |
| not-applicable | Hop cannot exist for this technology class |

Never promote `inferred` to `established` because the narrative is tidy.

## Evidence problems by arrow

Treat each arrow as a different failure mode. Details and queries are in sources.md.

- Grant → Research — award exists; stated aim may not match later papers.
- Research → Publication — acknowledgment strings are messy; not every paper lists the grant.
- Publication → Inventor — authors ≠ inventors; order and legal names drift.
- Inventor → Patent — not every invention is filed; provisionals vanish; continuations fork the family.
- Patent → Assignment — USPTO assignment text is noisy; security agreements look like ownership changes.
- Assignment → License — licenses are usually private. Absence of a recorded license is not proof of no license.
- License → Company — exclusive vs non-exclusive vs option vs inter-institutional agreement.
- Company → Product — patent-to-product mapping is the weakest public hop. Require a label, 510(k), Orange Book, standard-essential declaration, or vendor claim tied to a patent number.
- Product → Revenue / acquisition / procurement — company-level money is not product-level money unless the filing says so.

## Output

Write to `artifacts/<slug>/` unless the user names another folder.

Required files:

- `PROVENANCE.md` — human report from the template
- `provenance.json` — machine graph
- `GAPS.md` — every unresolved hop and the next public record that would close it
- `SOURCES.md` — URLs and retrieval dates actually used

Optional: mermaid of the joined money + knowledge graph. Keep node ids identical to `provenance.json`.

## Do

- Search public systems in the order listed in sources.md
- Quote government-interest clauses and assignment conveyance text when present
- Keep inventor, assignee, licensee, and product owner as separate nodes
- Record negative searches ("PatentsView inventor+assignee query returned 0") so the next agent does not pretend the hop was not tried
- Mark paywalled or credentialed systems (`iEdison`, most TTO license ledgers, Crunchbase Pro) as `unresolved` with `identifier: search:<system>` rather than guessing
- Point every unresolved edge at a `gaps[]` hop of `from|type|to`

## Do not

- Treat a university press release as an assignment
- Treat a co-author as an inventor
- Treat a forward citation as proof of funding lineage
- Treat SBIR Phase II plus a later product as proof the product embodies the award
- Compute "taxpayer ROI" or allege improper privatization
- Claim complete coverage of an agency, country, or technology class
- Use ticker symbols, emails, or scraped employee names as primary keys
- Merge entities that share a brand but not a legal person

## Sister skills

If a fund-tracking skill exists in the session, this skill owns the knowledge/IP graph and the join keys. The fund skill owns appropriation → agency → obligation → outlay. Neither skill may invent the other's identifiers.
