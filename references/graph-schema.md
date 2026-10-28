# Graph schema

Node and edge ids are stable slugs. Do not reuse an id for a different legal person.

## Node types

| type | required fields | notes |
|---|---|---|
| grant | `id`, `fain_or_award_id`, `agency`, `recipient_id` | One award. Competing renewals are separate nodes with a `continuation_of` edge |
| recipient | `id`, `legal_name`, `uei` | Prime awardee |
| subrecipient | `id`, `legal_name`, `parent_award_id` | |
| person | `id`, `name`, `role[]` | Roles include `pi`, `inventor`, `founder`. Same human may hold several |
| publication | `id`, `doi` or `pmid`, `year` | |
| invention | `id`, `disclosure_ref?` | Use only when a public disclosure or iEdison-equivalent exists |
| patent | `id`, `country`, `number`, `kind`, `family_id?` | Applications and grants are separate nodes linked by `matures_to` |
| assignment | `id`, `reel_frame?`, `recorded_at`, `conveyance` | |
| license | `id`, `exclusivity`, `licensor_id`, `licensee_id` | Most will stay `unresolved` |
| organization | `id`, `legal_name`, `jurisdiction` | University, TTO, company, acquirer |
| product | `id`, `name`, `regulator_id?` | |
| capital_event | `id`, `kind`, `amount?`, `date` | kind = seed / series / debt / grant-follow-on / ipo |
| acquisition | `id`, `acquirer_id`, `target_id`, `date` | |
| procurement | `id`, `buyer`, `piid`, `amount?` | Government purchase of a product or from a company |

`id` format: `type:stable-slug` — e.g. `grant:nih-r01-ca123456`, `patent:us-12345678-b2`.

## Edge types

| type | from → to | required on the edge |
|---|---|---|
| funds | grant → recipient | amount, instrument (grant/contract/coop) |
| subawards | recipient → subrecipient | amount if published |
| employs_or_appoints | organization → person | role, dates if known |
| acknowledges | publication → grant | snippet of funding statement |
| authors | person → publication | |
| invents | person → patent or invention | |
| discloses | invention → patent | |
| matures_to | application → grant | |
| continuation_of | patent → patent | |
| cites | patent → patent | never used alone as funding proof |
| owned_by | patent → organization or person | as_of |
| assigned_by | assignment → from party | |
| assigned_to | assignment → to party | |
| government_interest | patent → grant or agency | quoted clause |
| licenses | organization → organization | exclusivity, field, territory if known |
| options | organization → organization | expiry if known |
| spins_out | organization → organization | |
| embodies | product → patent | only with a product-patent source |
| sells | organization → product | |
| procures | agency → product or organization | |
| acquires | organization → organization | |
| invests | organization → organization | via capital_event |

Every edge must include:

```
confidence: established | corroborated | inferred | unresolved | not-applicable
source: URL or registry name
identifier: the record id at that source
as_of: ISO date of the record or of retrieval
note: optional, one sentence
```

## Join keys to a financial graph

Share these ids verbatim if a fund-tracking graph exists:

- `grant.id` / FAIN
- `recipient.uei`
- `subrecipient.id`
- procurement `piid`

Do not join on agency display name, city, or ticker.

## Provenance JSON envelope

```json
{
  "schema": "public-innovation-provenance.v1",
  "seed": {"type": "grant", "id": "grant:nih-r01-ca123456"},
  "direction": ["forward"],
  "generated_at": "2026-09-28",
  "nodes": [],
  "edges": [],
  "public_return": [],
  "gaps": []
}
```

`direction` is `forward`, `reverse`, or both. Validate with `scripts/check-provenance.py`.
