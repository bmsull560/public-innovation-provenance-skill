# Reverse traversal

Seed is a patent, family, company, or product. Goal is to find public-funding ancestors without fabricating a grant number.

## Patent or application seed

1. Read the government-interest / federally sponsored research section. Quote it. Parse agency and award ids if present. This hop is `established` when the clause exists.
2. Pull the family (US continuations, WO, EP). Government-interest often appears on one sibling only. Copy the clause to the family with `corroborated` if siblings share inventors and priority, else keep it on the marked document.
3. List inventors. Search USPTO / PatentsView for other patents by the same inventor + employer around the priority year.
4. Match inventor legal names to publications in OpenAlex / PubMed in a ±3 year window on the same CPC / MeSH neighborhood.
5. From those papers, harvest grant acknowledgments. A grant on a paper by the inventors is `corroborated` only if the paper's technical claims overlap the patent's first independent claim in plain language you can quote. Otherwise `inferred` and say why.
6. Check NIH RePORTER patents tab, NSF results, DOE OSTI, SBIR award pages for the inventor or the first assignee.
7. Walk assignments backward. A university assignee plus a later company assignee is a commercialization clue, not a grant.

Do not treat a citation to a federally funded paper as proof this patent was federally funded.

## Company seed

1. Resolve the legal entity (jurisdiction + SOS record + UEI if any). Brand names are not entities.
2. Collect patents assigned to that entity and to known predecessors (merger assignments).
3. Run the patent procedure on each family. Cap at the families the user named, or the top families by explicit product linkage if they asked for the company as a whole. State the cap.
4. Search USAspending and SBIR.gov for the UEI / legal name as recipient.
5. Search USAspending contracts and SAM for the same firm as vendor. Procurement is a public-return cell, not proof of origin.
6. Founders vs inventors — same person is a join key only after name + employment overlap is documented.

A company that once received an SBIR and later sells a product has two public facts. The `embodies` edge between them stays `unresolved` until a patent, label, or contract SOW ties them.

## Product seed

1. Capture trade name and every regulatory number (NDA, ANDA, BLA, 510(k), PMA, device listing, USDA, FCC).
2. Orange Book / device label / 510(k) summary often lists patents or predicates. Those patents become the new seeds.
3. If no patent list exists, search assignee + product keywords. Hits are `inferred`.
4. Then run the patent procedure.

## Stopping rules

- Stop a branch after two consecutive `inferred` hops. Write the gap.
- Stop when government-interest names an award and that award is resolved in USAspending or the agency reporter.
- Do not walk citation graphs more than one hop looking for funding.

## Worked pattern (shape only)

```
product:orpha-drug
  └─ embodies (Orange Book) → patent:us-#########
       ├─ government_interest (face) → grant:nih-r01-…
       └─ assigned_to → org:univ-x
            └─ licenses (10-K exhibit) → org:co-y
                 └─ sells → product:orpha-drug
```

Every one of those edges still needs `source`, `identifier`, `as_of`, `confidence`.
