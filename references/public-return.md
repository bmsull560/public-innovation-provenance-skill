# Public-return ledger

Accounting and evidence. Not a score, grade, or moral. Fill every row. Use `not-applicable` when the technology class cannot have that row (e.g. FDA approval for a pure software library).

| Dimension | Question | Typical public source | Allowed answers |
|---|---|---|---|
| Public funding | How much government money supported the research? | USAspending obligation / outlay, agency reporter | amount + currency + award ids, or unresolved |
| Research output | What was produced? | RePORTER pubs, OpenAlex, data repos | list of publication / dataset ids |
| IP | What IP resulted? | PatentsView, agency patent tabs | patent / application / software / data nodes |
| Ownership | Who holds title as of the report date? | USPTO assignment chain | owner node + as_of |
| Government license | Is a federal paid-up license asserted on the patent? | government-interest clause | quoted clause or unresolved |
| Licensing | Who received commercialization rights? | EDGAR exhibits, TTO pages (weak) | licensee + exclusivity + confidence |
| Commercialization | What product or company resulted? | labels, IR, SOS | product / org nodes |
| Capitalization | Did the company raise private capital later? | EDGAR, state filings | capital_event or unresolved |
| Acquisition | Was the company or the family acquired? | EDGAR, assignment merger | acquisition node or none-found |
| Government use | Does government buy the resulting product or contract the firm? | USAspending contracts, SAM | procurement nodes; do not assume they buy *this* IP |
| Public access | Are papers, data, or tools publicly available? | PMC, agency public-access policy, repos | yes / mixed / unresolved with links |
| Revenue | Is commercial revenue publicly observable? | 10-K product-line, not press ARR | figure with filing cite, or unresolved |
| Royalty | Is institutional royalty participation visible? | foundation reports, rare 990 notes | figure or unresolved — never "none" |
| Follow-on public funding | Did the same technology receive later public money? | later awards to same core project, SBIR phases | grant nodes |

## Rules for amounts

- Keep obligation and outlay distinct. Do not add them.
- Do not sum awards across an inventor's whole career and call it "this product's public funding."
- Do not subtract private capital from public awards.
- Do not compute a ratio labeled ROI, bang-for-buck, or taxpayer return.
- Inflation-adjust only if the user asks, and name the deflator.

## Narrative discipline

Allowed: "Award R01-CA123456 obligated $1.2M. Patent US########## names that award in the government-interest clause. Exclusive license text is not public."

Forbidden: "Taxpayers funded it and the company captured the upside."
