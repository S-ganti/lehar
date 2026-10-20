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

## Known issues (shipped as is, 20 Oct 2026)

From the second finish review; the decision was to ship and fix later.

- **Contour labels can overprint company labels.** The lettering along the isochrones ("≥15% of costs or revenue") is not part of the map's label collision avoidance; on desktop it can run through the Asian Paints and Reliance labels, and the 5–15% label can sit near vertical. Fix: add contour labels to the collision set, or place each on a clear stretch of its line with rotation capped at about ±30°.
- **Third fund's route colour is too close to "held directly".** In "What you really own", the third fund in a portfolio (HDFC Mid Cap in the sample) gets #155150, which reads as the direct-holding ink. Fix: use a mid-light teal step for the third fund, or a pattern.
- **"What moved" is unreadable on phones.** The timeline is one SVG scaled to the screen, so at 390 px its labels are about 4 px. Fix: a stacked row layout under 720 px, or the chart at a readable scale with horizontal scroll.

## Not yet decided

Name (Lehar is a working name), pricing, which funds to add next, and a legal view on the what-if arithmetic under SEBI's research analyst rules. See `PRODUCT.md`.
