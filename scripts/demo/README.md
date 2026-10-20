# Lehar data

`index.html` reads `data/demo/demo.json` plus `data/latest.json`. Rebuild `demo.json` with:

```bash
python scripts/demo/build_demo.py
```

## Inputs and where they come from

| File | Source | Refresh |
|---|---|---|
| `data/demo/nifty200.csv`, `nifty500.csv` | NSE index constituent lists, niftyindices.com `/IndexConstituent/ind_nifty200list.csv` and `ind_nifty500list.csv` | When the index rebalances (semi-annual) |
| `data/demo/amfi_industry.json` | AMFI industry per ISIN, from the HDFC Nifty500 Multicap 50:25:25 Index Fund monthly portfolio (it holds the whole Nifty 500) | Monthly, with fund data |
| `data/demo/funds.json` | Each AMC's own monthly portfolio disclosure: PPFAS (amc.ppfas.com), HDFC (hdfcfund.com) | Monthly; AMCs publish by about the 10th |
| `data/demo/curated.json` | Cost and revenue shares for 73 companies, curated from annual reports (exported once from Risk Radar) | When the curated map changes |

Fund files are read in the browser from the AMC's own page and parsed in memory (no file saved), dumped row by row, then parsed with
`scripts/demo/parse_fund_dump.py <dump.txt> <fund_id> "<name>" <asof> <source url>`.

**Check after every refresh:** each fund's parsed totals should match the sub-totals in its own disclosure.
For 30 Sep 2026 they did: PPFAS Flexi Cap (equity 72.06%, arbitrage 1.44%, REITs 6.27%, foreign 11.90%, money market 3.87%),
HDFC Flexi Cap 94.97%, Mid Cap 91.71%, Large Cap 98.37%, Nifty 50 Index 100.04%.

## What the exposures mean
- **company**: cost-base shares (and revenue shares for producers) estimated from the company's annual report. Estimates.
- **sector**: what is typical for the company's AMFI industry. A direction and a level, not a measurement.
- Arbitrage positions are excluded from exposure: they are offset by short futures in the same fund.
- Nothing here is a buy/sell/hold view or a price forecast; the what-if shows cost or revenue arithmetic only.
