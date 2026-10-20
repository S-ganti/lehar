---
version: 1
slug: "index-html"
primary_target: "index.html"
related_targets: []
---

# Surface brief: index.html (Lehar portfolio exposure map)

Scope: the single product page, index.html. Visitor mode: Operate (a working tool), first viewport demonstrates the mechanism on a sample portfolio.

Audience and job: salaried self-directed investors (mostly mutual funds plus a few stocks) checking what their money is exposed to when crude, the rupee or a policy moves; secondary, creators and advisors screen-sharing it. Task: see what they really own, which factors reach it, what a move would touch; then swap in their own holdings.

Content and proof: real data only (Nifty 500, AMFI industries, five funds' 30 Sep 2026 disclosures, 73 company cost maps, daily moves). Sample portfolio is labelled as a sample. No advice, no price forecasts, no invented users or claims.

Constraints: every function of the prototype stays (portfolio input with search and CSV paste, look-through with overlap, exposure for all factors, what moved with dates and staleness, what-if, coverage and sources). Avoid trading-app energy, consulting-report density, gamified fintech, generic SaaS dashboard. Holdings stay in the browser. Static HTML, no build step.

Memorable moment: picking a factor sends onset contours sweeping out from its origin across the map of your companies, each reached in turn and labelled with what changes for it.

## Direction contract

THESIS: A market move spreads through a portfolio the way the monsoon advances up India: an origin, dated onset contours, and places reached in order. Refuses the category default of KPI cards, a donut and a holdings table.

OWN-WORLD: IMD onset-map paper: pale green-grey map ground, deep monsoon-teal shell bar and ink, teal isochrone contours (solid for measured, dotted for template or stale), rainfall-band tints for reached zones; data colours only on data, IMD-style: deficit orange-red for cost, excess blue for revenue, violet for both ways, each also a fill pattern (solid, hatched, cross-hatched). One face, Anek Latin (Ek Type, Mumbai), its width axis doing cartographic work: condensed tracked caps for region labels, normal width for UI, tabular figures.

STORY: The visitor sees the sample portfolio already mapped, watches crude oil's onset reach 38% of the money, learns that it travels through their funds as well as their stocks, explores other factors and moves, then opens the portfolio drawer and replaces the sample with their own holdings.

FIRST VIEWPORT: Teal top bar: Lehar wordmark left, section nav (Map, What you own, All factors, What moved, Sources), sample-portfolio summary and the primary "Use my portfolio" button right. Below, two work areas: the onset map (about two-thirds width) with industries as named regions, companies as places sized by your money, the origin pin bottom-left and contours sweeping out; and a right panel with the factor list (each with its share of your money), the move slider, the headline "Crude oil reaches 38% of your money", and the reached companies as a ranked list with what changes for each.

FORM: Monsoon onset map (IMD isochrone tradition); position 1 on the ordered grounded list (Impeccable's pick, chosen by the user over the assigned Mandi Rate Board); seed key 79fcba83. Kept from the declined hand: fixed furniture on every holding (character catalog), hairline density without card inflation (Japanese high-density web), one geometry for contours, layout and state (zoo guide map), colour quarantined to data (lexicon), meaning carried by pattern as well as colour (darkroom record).

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
