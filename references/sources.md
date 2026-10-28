# Public sources by hop

Search in this order. Prefer primary registries over journalism. Record the URL and retrieval date in `SOURCES.md`.

## Grant → Research

| System | What it proves | Id to capture |
|---|---|---|
| [USAspending](https://www.usaspending.gov/) + [API](https://api.usaspending.gov/) | FAIN, awarding agency, recipient UEI, obligation/outlay, subawards, NAICS/PSC | FAIN, award id, UEI |
| [NIH RePORTER](https://reporter.nih.gov/) + [API](https://api.reporter.nih.gov/) | Activity code, serial, PIs, project title, pubs, patents linked by NIH | core project number |
| [NSF Award Search](https://www.nsf.gov/awardsearch/) | Award id, PI, abstract, publications when filed | NSF award number |
| [SBIR.gov](https://www.sbir.gov/) | Agency, firm, phase, topic, award amount | SBIR award / contract |
| [SAM.gov](https://sam.gov/) | Entity legal name, UEI, exclusion status | UEI |
| [Grants.gov](https://www.grants.gov/) | Opportunity, CFDA/ALN, agency program | opportunity number |
| NASA TechPort, DOE OSTI / PAGE S, USDA NIFA Reporter, DoD award announcements | Agency-specific project records | agency project id |
| [CORDIS](https://cordis.europa.eu/) | EU / Horizon grant, participants, results | grant agreement id |

Capture at minimum: grant number, funding agency, program / ALN, recipient legal name, UEI, PIs, period of performance, obligated amount, outlayed amount if published, stated objective.

Subawards are first-class nodes. Do not fold a subrecipient into the prime.

## Research → Publication

| System | What it proves |
|---|---|
| [PubMed](https://pubmed.ncbi.nlm.nih.gov/) / PMC | PMID, grant in secondary source or PMC funding |
| [OpenAlex](https://openalex.org/) | DOI, authorship, funder ids, referenced works |
| [Europe PMC](https://europepmc.org/) | Grant-article links, including NIH and EU |
| NIH RePORTER publications tab | Agency-asserted paper list for that core project |
| Crossref funder registry | Funder DOI on the article, not the grant number |

A paper that does not name the grant is not proof the grant did not fund it. Mark as `inferred` only when author, year, and topic align and say so. Otherwise `unresolved`.

## Publication / inventor → IP

| System | What it proves |
|---|---|
| [PatentsView](https://patentsview.org/) | Inventor names, assignees, CPC, citations, government interest flag |
| [USPTO Patent Center](https://patentcenter.uspto.gov/) / Public PAIR remnants | Application, continuity, assignments docket |
| [Google Patents](https://patents.google.com/) | Full text, government-interest section, family |
| [EPO Espacenet](https://worldwide.espacenet.com/) | WO / EP family, applicants |
| Agency invention reports | NIH RePORTER patents tab; some DOE / NASA result pages |

`iEdison` is the federal invention-reporting system under Bayh-Dole. It is not a public search engine. Treat unreported-but-likely inventions as `unresolved`, never as absence of IP.

Government-interest text on the face of a US patent is the strongest public reverse link. Quote it.

## IP → Ownership

| System | What it proves |
|---|---|
| [USPTO Assignment Search](https://assignment.uspto.gov/) | Recorded conveyance, reel/frame, assignor, assignee, date |
| Patent front page | Current assignee at grant — not the live owner |
| University TTO invention / license catalogs | Marketing claims; corroborate before promoting |
| SEC EDGAR (10-K, S-1 risk factors, exhibits) | Material exclusive licenses sometimes disclosed |
| Court dockets (PACER / CourtListener) | Ownership fights, march-in related filings |

Read conveyance type. "Security agreement" and "change of name" are not assignments of title. "Nunc pro tunc" backdates; keep both recorded date and purported effective date.

## IP → Commercialization

| System | What it proves |
|---|---|
| FDA [openFDA](https://open.fda.gov/), Orange Book, 510(k), PMA, BLA labels | Regulatory owner, sometimes patent numbers |
| ClinicalTrials.gov | Sponsor, intervention, listed grant or collaborator |
| SAM.gov contract awards + USAspending contracts | Government as customer of a company, not proof of this patent |
| SEC EDGAR | Product lines, acquisitions, license exhibits |
| Company IR / legal name filings | Product claims; treat as self-assertion |
| Standards bodies / IEEE / IETF | SEP declarations tying patents to products |
| State SOS entity search | Spinout formation date and officers vs inventor names |

Capital raises and acquisitions are company events. Attach them to the company node. Only attach to a patent when the filing names that family.

## Negative-search log

For every hop tried and missed, write one line:

```
unresolved | patent→license | USPTO assignment + EDGAR exhibit search | 2026-09-28 | 0 recorded exclusive licenses
```

That line is part of the pack, not scrap.
