# Lehar

See where a market move reaches your money.

Lehar opens your mutual funds into the companies they hold, adds your direct stocks, and maps every company to what moves its costs or revenue: crude oil, the rupee, metals, gas, edible oils, interest rates. Pick a factor and watch its onset spread across the companies you own, the way the monsoon advances up the country.

Information only, built from public data. No buy, sell or hold views and no price forecasts.

## Run it

It is one static page that fetches two JSON files, so it needs a local web server (opening the file directly will not load the data):

```bash
python -m http.server 8788
```

Then open http://localhost:8788/.

## What is on the page

| View | What it shows |
|---|---|
| Onset map | Your companies as places grouped into industry regions, sized by your money. Choose a factor: the contours show how strongly it reaches each company (company estimate or industry template). |
| Panel | Factors ranked by how much of your money they reach, a move slider (what-if), and the reached companies with what changes for each (cost or revenue share × move). |
| What you really own | Asset mix, overlap ("you own HDFC Bank 3 ways"), and your biggest companies split by route: direct or through each fund. |
| All factors | Factors against your 22 biggest companies, as a grid. |
| What moved | The latest move for each factor, the window it was measured over and the date its data is from; older data is dotted. |
| Your portfolio | Search and add stocks or funds, or paste a list. Saved in your browser only. |
| How much is measured | Share of your money with company-level data, industry templates, or not mapped; sources. |

## Data

| File | What | Source |
|---|---|---|
| `data/demo/demo.json` | Built by `scripts/demo/build_demo.py`: Nifty 500 universe, exposures, fund holdings | below |
| `data/demo/nifty200.csv`, `nifty500.csv` | Index constituents | NSE, niftyindices.com |
| `data/demo/amfi_industry.json` | AMFI industry per ISIN | an index fund's 30 Sep 2026 monthly portfolio |
| `data/demo/funds.json` | Five funds' holdings, 30 Sep 2026 | each fund house's own monthly disclosure (PPFAS, HDFC) |
| `data/demo/curated.json` | Cost and revenue shares for 73 companies | estimated from annual reports; exported once from Risk Radar |
| `data/latest.json` | Latest moves, dates, staleness | snapshot of the Risk Radar daily feed (19 Oct 2026) |

Refresh steps and the checks to run are in `scripts/demo/README.md`. Fund disclosures come out around the 10th of each month.

`data/latest.json` is a snapshot, not a live feed. Wiring a daily refresh into this repo is still to do.

## Fixed since first release (21 Oct 2026)

- Contour labels are now straight text on the clearest stretch of each line (rotation capped at 30°) and are part of the map's label collision set, so they no longer print over company labels.
- Fund route colours follow the documented teal steps; the third fund no longer looks like "held directly".
- "What moved" is a stacked list on phones (720 px and below), with readable text and tappable rows.

## Not yet decided

Name (Lehar is a working name), pricing, which funds to add next, and a legal view on the what-if arithmetic under SEBI's research analyst rules. See `PRODUCT.md`.
