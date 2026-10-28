# Density bar (synthetic)

This example is shaped like a real pack. Do not copy the fake identifiers into a live report.

Seed: `grant:nih-r01-xx000001`. Direction: forward.

Established hops:

- USAspending FAIN `R01XX000001` obligated `USD 1_200_000` to `recipient:state-u` (UEI documented).
- RePORTER lists two PMIDs that acknowledge the core project.
- US `9,000,001` government-interest clause names `NIH` and `R01XX000001`.
- USPTO assignment reel/frame transfers title from the two inventors to `organization:state-u`.

Corroborated:

- Later assignment of the same patent to `organization:spinco` after a TTO press note that a startup licensed the family. Press note alone would have been inferred; assignment promotes the ownership hop, not the license terms.

Unresolved:

- Exclusive vs non-exclusive license text
- Royalty participation
- Whether FY2024 DoD contracts to SpinCo purchase a product that embodies `9,000,001`

Inferred (must stay labeled):

- Product page for `SpinPrep` mentions "our patented sample-prep chemistry" with no patent number. `embodies` edge exists only as inferred, or is omitted.

Public-return excerpt:

- Public funding — `USD 1_200_000` obligated, outlay not separately published — established
- Government license — clause quoted — established
- Royalty — no public ledger — unresolved
- Government use — contracts exist to the firm, not tied to this family — inferred, with that caveat in the finding

Two consecutive inferred hops would have stopped the branch.
