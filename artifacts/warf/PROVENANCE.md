# Public innovation provenance — WARF portfolio (priority companies)

Generated 2026-11-02. Direction forward + reverse. Confidence vocabulary: established / corroborated / inferred / unresolved / not-applicable.

Research cutoff: 2026-11-02. Any later evidence labeled separately.

## Seed

- Type: institution
- Canonical id: org:warf
- Aliases: Wisconsin Alumni Research Foundation
- Question: Which publicly supported inventions reached which portfolio companies through documented rights and ownership, and what financial flows or public benefits can be established?

## Chain (short)

Government funding → research → IP (WARF patents) → ownership → license → company → commercialization. Most license schedules and exact covered-patent mappings remain unresolved.

## Nodes

| id | type | label | primary identifier |
|---|---|---|---|
| org:warf | organization | Wisconsin Alumni Research Foundation | — |
| org:shine | organization | SHINE Technologies, LLC | — |
| org:alithic | organization | Alithic (formerly Earth RepAIR) | — |
| org:realta | organization | Realta Fusion, Inc. | — |
| patent:us10332646b2 | patent | Apparatus and method for generating medical isotopes | US10332646B2 |
| patent:us11238999b2 | patent | Apparatus and method for generating medical isotopes | US11238999B2 |
| patent-app:p220309us02 | patent | Cementitious materials... | P220309US02 (university technology reference; publication status unresolved) |
| grant:de-ar0002077 | grant | ARPA-E REDUCE | DE-AR0002077 |

## Edges

| from | type | to | confidence | source | identifier | as_of |
|---|---|---|---|---|---|---|
| org:shine | licenses | org:warf | corroborated | SHINE 2017 release | SHINE-2017-09-28 | 2017-09-28 |
| patent:us10332646b2 | owned_by | org:warf | established | USPTO | US10332646B2 | 2019-06-25 |
| patent:us11238999b2 | owned_by | org:warf | established | USPTO | US11238999B2 | 2022-02-01 |
| grant:de-ar0002077 | funds | org:shine | established | USAspending | DE-AR0002077 | 2025-09-14 |
| patent-app:p220309us02 | owned_by | org:warf | established | WARF listing | P220309US02 | 2025-02-19 |

## Public-return ledger

See provenance.json for full 14 dimensions. Key points:

- Public funding: established for DE-AR0002077 (SHINE); university-reported $2.3M DOE for Alithic (award ID unresolved); Realta awards from prior pack.
- Licensing: company statement of exclusive worldwide licenses for accelerator technology and two WARF-managed patents (exact numbers unresolved). “Managed by WARF” does not independently establish ownership.
- Government license: confirmatory license on Realta WARF patent; none identified for SHINE candidates in this pass.
- No patent-to-product embodiment established; commercialization outcomes separate.

## Gaps

See GAPS.md. Highest value: SHINE patent schedule, Alithic patent numbers + DOE award ID, Realta executed TIA/IP exhibits.

## Negative searches

- Exact patent numbers in SHINE–WARF accelerator license: not in 2017 release or subsequent public company materials examined.
- Confirmatory-license recordings on US10332646B2 / US11238999B2: not located in public assignment records in this pass.
- Alithic DOE award identifier: not in university reporting examined.
- PatentsView bulk queries: unavailable; record-level alternatives used.

## What this pack does not claim

- That any specific patent is covered by the SHINE or Alithic licenses (candidates only).
- Any dollar ratio or return calculation.
- Completeness of the portfolio or of federal awards.
- That portfolio membership establishes a patent license.
