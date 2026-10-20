#!/usr/bin/env python3
"""
Build data/demo/demo.json for Lehar (index.html).

Joins four sources and keeps each figure's basis visible:

  1. Index membership: NSE Nifty 200 and Nifty 500 constituent lists (niftyindices.com).
  2. Industry: AMFI industry classification per ISIN, read from the 30 Sep 2026
     monthly portfolio of an index fund that holds the whole Nifty 500.
  3. Exposures:
       - basis "company": the curated cost-base map in data/demo/curated.json (exported
         from Risk Radar), estimated from annual-report disclosure. Numeric cost shares.
       - basis "sector": an industry template, describing exposures typical of the
         business. Levels only (high / medium / low), never presented as company-specific.
  4. Fund holdings: monthly portfolio disclosures from each AMC's own site (funds.json).

No buy/sell/hold views, no price targets. The demo shows what a company's cost base
or revenue is exposed to, and how much of a portfolio sits in those companies.

run: python scripts/demo/build_demo.py
"""
import csv
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEMO = os.path.join(ROOT, "data", "demo")

# ---------------------------------------------------------------------------
# Drivers: the things that move. 'series' names the field in data/latest.json
# (moves/vols) where a real price series exists; None = what-if only.
# ---------------------------------------------------------------------------
DRIVERS = {
    "crude":  {"n": "Crude oil", "series": "crude", "unit": "Brent, USD/bbl",
               "note": "Includes crude-derived inputs: fuels, plastics, petrochemicals, carbon black, synthetic rubber."},
    "gas":    {"n": "Natural gas / LNG", "series": "natgas", "unit": "Henry Hub, USD/MMBtu",
               "note": "Series is US Henry Hub. India's LNG is partly oil-indexed and partly priced off Asian spot (JKM), so read moves with care."},
    "coal":   {"n": "Coal", "series": "coal", "unit": "Australian thermal coal, monthly",
               "note": "Thermal coal series. Coking coal (steel) moves on its own curve and has no free series."},
    "steel":  {"n": "Steel and iron ore", "series": "ironore", "unit": "Iron ore, monthly",
               "note": "Iron ore used as the closest free series for the steel chain. Indian steel prices also move on domestic demand and duties."},
    "copper": {"n": "Copper", "series": "copper", "unit": "Copper, monthly", "note": ""},
    "alum":   {"n": "Aluminium", "series": "alum", "unit": "Aluminium, monthly", "note": ""},
    "gold":   {"n": "Gold and silver", "series": "gold", "unit": "LBMA gold, USD/oz",
               "note": "In India the landed price also includes import duty (15% since 13 May 2026)."},
    "edoil":  {"n": "Edible oils", "series": "palm", "unit": "Palm oil, monthly",
               "note": "Palm oil series; soy and sunflower oil usually move with it."},
    "rubber": {"n": "Natural rubber", "series": "natrub", "unit": "Rubber, monthly", "note": ""},
    "sugar":  {"n": "Sugar", "series": "sugar", "unit": "Sugar, monthly",
               "note": "Indian sugar prices are largely set by policy (MSP, export quotas, ethanol diversion), not by the world price."},
    "grains": {"n": "Wheat and grains", "series": "wheat", "unit": "Wheat, monthly",
               "note": "India's wheat market is closed to exports; domestic prices follow procurement policy more than world prices."},
    "softs":  {"n": "Cocoa, coffee, tea", "series": "cocoa", "unit": "Cocoa, monthly", "note": ""},
    "usd":    {"n": "Rupee vs dollar", "series": "usdinr", "unit": "USD/INR",
               "note": "A rise in USD/INR means a weaker rupee: it helps companies earning in dollars and hurts those paying in dollars."},
    "rates":  {"n": "Interest rates", "series": None, "unit": "RBI policy rate / bond yields",
               "note": "No rate series in the feed yet; what-if only."},
    "power":  {"n": "Electricity", "series": None, "unit": "Industrial power tariff",
               "note": "Indian grid is ~70% coal-fired; no free industrial-tariff series."},
    "other":  {"n": "Other inputs (no price feed)", "series": None, "unit": "",
               "note": "Inputs with no free price series: APIs from China, chips, lithium, titanium dioxide, palladium, cotton, pulp and others."},
}

# Dashboard commodity id -> driver
COM_DRIVER = {}
for d, ids in {
    "crude": "crude dubai diesel jet gasoline naphtha lpg petcoke bitumen plastics ethylene propylene benzene pta meg pvc "
             "styrene vam carbonblack sbr phenol bunker caustic",
    "gas": "natgas lng apmgas ttf ammonia urea methanol",
    "coal": "coal metcoal",
    "steel": "ironore steel hrc scrap ferroalloy",
    "copper": "copper",
    "alum": "alum alumina bauxite",
    "gold": "gold silver",
    "edoil": "palm soyoil sunoil mustard copra",
    "rubber": "natrub",
    "sugar": "sugar ethanol",
    "grains": "wheat rice maize",
    "softs": "cocoa coffee tea",
    "power": "elec",
}.items():
    for i in ids.split():
        COM_DRIVER[i] = d

# ---------------------------------------------------------------------------
# Sector templates by AMFI industry. Each entry: driver, effect, level, why.
# effect: "cost" (higher price hurts margins), "benefit" (higher price helps), "mixed".
# For "usd", effect refers to a WEAKER rupee (USD/INR up).
# ---------------------------------------------------------------------------
T = {
    "Banks": [("rates", "mixed", "high", "Higher rates lift loan yields but raise deposit costs and credit stress")],
    "Finance": [("rates", "cost", "high", "Lenders funded by borrowing: higher rates raise funding cost")],
    "Insurance": [("rates", "mixed", "medium", "Bond-heavy investment books: yields change both returns and reported values")],
    "Capital Markets": [("rates", "mixed", "low", "Activity-driven revenue; rates matter through market sentiment")],
    "Financial Technology (Fintech)": [("rates", "mixed", "low", "Lending partners and funding costs move with rates")],
    "IT - Software": [("usd", "benefit", "high", "Most revenue billed in dollars, costs mainly in rupees")],
    "IT - Services": [("usd", "benefit", "high", "Most revenue billed in dollars, costs mainly in rupees")],
    "Pharmaceuticals & Biotechnology": [("usd", "benefit", "medium", "Large share of revenue from exports, largely in dollars"),
                                        ("other", "cost", "medium", "APIs and key starting materials, largely imported from China"),
                                        ("crude", "cost", "low", "Solvents and packaging")],
    "Healthcare Services": [("usd", "cost", "low", "Imported medical equipment")],
    "Electrical Equipment": [("copper", "cost", "high", "Copper windings, cables and conductors"),
                             ("steel", "cost", "medium", "Electrical steel and structures"),
                             ("alum", "cost", "medium", "Aluminium conductors and housings")],
    "Industrial Products": [("steel", "cost", "medium", "Steel is a main material input"),
                            ("copper", "cost", "medium", "Copper and brass for cables, pipes and components")],
    "Industrial Manufacturing": [("steel", "cost", "medium", "Steel fabrication and machinery inputs")],
    "Aerospace & Defense": [("alum", "cost", "low", "Aluminium alloys"), ("steel", "cost", "low", "Special steels")],
    "Power": [("coal", "cost", "medium", "Thermal generation fuel; regulated tariffs pass much of it through, with a lag")],
    "Retailing": [("crude", "cost", "low", "Logistics and packaging")],
    "Consumer Durables": [("copper", "cost", "medium", "Copper in motors, compressors and wiring"),
                          ("steel", "cost", "medium", "Steel bodies and frames"),
                          ("crude", "cost", "low", "Plastic housings and packaging")],
    "Automobiles": [("steel", "cost", "high", "Steel is the largest material input"),
                    ("alum", "cost", "medium", "Aluminium castings and parts"),
                    ("crude", "cost", "medium", "Plastics and rubber parts; fuel prices also shape demand"),
                    ("rubber", "cost", "low", "Tyres and rubber parts")],
    "Auto Components": [("steel", "cost", "medium", "Steel forgings, castings and stampings"),
                        ("alum", "cost", "medium", "Aluminium die-castings"),
                        ("crude", "cost", "low", "Plastics and rubber")],
    "Agricultural, Commercial & Construction Vehicles": [("steel", "cost", "high", "Steel is the largest material input"),
                                                         ("crude", "cost", "low", "Diesel prices shape fleet demand")],
    "Realty": [("rates", "cost", "high", "Home-loan rates drive demand; developer debt costs"),
               ("steel", "cost", "low", "Construction steel")],
    "Construction": [("steel", "cost", "high", "Steel and cement are the largest bought-out materials"),
                     ("crude", "cost", "medium", "Diesel and bitumen")],
    "Cement & Cement Products": [("coal", "cost", "high", "Kiln fuel (coal and petcoke)"),
                                 ("crude", "cost", "medium", "Petcoke and diesel freight"),
                                 ("power", "cost", "medium", "Grinding is power-intensive")],
    "Non - Ferrous Metals": [("alum", "benefit", "high", "Sells aluminium, copper or zinc at LME-linked prices"),
                             ("coal", "cost", "medium", "Smelters run on coal-fired captive power")],
    "Diversified Metals": [("alum", "benefit", "high", "Sells metals at LME-linked prices"),
                           ("coal", "cost", "medium", "Captive power fuel")],
    "Ferrous Metals": [("steel", "benefit", "high", "Sells steel; realisations follow steel prices"),
                       ("coal", "cost", "high", "Coking coal, largely imported")],
    "Minerals & Mining": [("steel", "benefit", "high", "Sells iron ore")],
    "Metals & Minerals Trading": [("coal", "mixed", "medium", "Coal trading and mining")],
    "Consumable Fuels": [("coal", "benefit", "high", "Sells coal")],
    "Petroleum Products": [("crude", "mixed", "high", "Refiners: crude is the main cost; margins depend on the spread to fuel prices")],
    "Oil": [("crude", "benefit", "high", "Produces and sells crude oil"), ("gas", "benefit", "medium", "Produces natural gas")],
    "Gas": [("gas", "cost", "high", "Buys LNG and domestic gas to distribute")],
    "Telecom - Services": [("power", "cost", "low", "Network energy (grid and diesel)"), ("usd", "cost", "low", "Imported network equipment")],
    "Telecom - Equipment & Accessories": [("copper", "cost", "medium", "Copper and fibre cable inputs")],
    "Leisure Services": [("crude", "cost", "low", "Energy and travel costs")],
    "Personal Products": [("edoil", "cost", "medium", "Palm and other oils for soaps and creams"),
                          ("crude", "cost", "low", "Packaging")],
    "Diversified FMCG": [("edoil", "cost", "medium", "Palm oil derivatives"), ("crude", "cost", "low", "Packaging"),
                         ("grains", "cost", "low", "Wheat and other farm inputs")],
    "Agricultural Food & Other Products": [("edoil", "cost", "medium", "Edible oils"), ("softs", "cost", "medium", "Tea, coffee and other crops")],
    "Food Products": [("grains", "cost", "medium", "Wheat and other grains"), ("sugar", "cost", "medium", "Sugar"),
                      ("edoil", "cost", "medium", "Edible oils"), ("softs", "cost", "low", "Cocoa, coffee, dairy")],
    "Beverages": [("sugar", "cost", "medium", "Sugar"), ("crude", "cost", "low", "PET packaging"),
                  ("grains", "cost", "low", "Grain-based spirits and malt")],
    "Cigarettes & Tobacco Products": [("other", "cost", "low", "Leaf tobacco; taxation matters far more than input prices")],
    "Chemicals & Petrochemicals": [("crude", "cost", "high", "Crude-derived feedstocks")],
    "Fertilizers & Agrochemicals": [("gas", "cost", "medium", "Gas feedstock for nitrogen fertilisers; subsidies offset part of it"),
                                    ("crude", "cost", "low", "Petrochemical intermediates")],
    "Transport Infrastructure": [("crude", "cost", "low", "Fuel for port and airport operations")],
    "Transport Services": [("crude", "cost", "high", "Fuel is a large share of operating cost")],
    "Textiles & Apparels": [("other", "cost", "high", "Cotton yarn and fibre"), ("usd", "benefit", "low", "Export revenue")],
    "Paper, Forest & Jute Products": [("other", "cost", "high", "Wood pulp")],
    "Commercial Services & Supplies": [],
    "Household Products": [("crude", "cost", "medium", "Surfactants and packaging")],
    "Media": [],
    "Entertainment": [],
    "Other Utilities": [],
    "Other Consumer Services": [],
    "Engineering Services": [("usd", "benefit", "medium", "Export revenue")],
    "Capital Goods": [("steel", "cost", "medium", "Steel is a main material input")],
    "Telecommunication": [("copper", "cost", "medium", "Copper and optical-fibre cable inputs")],
    "Telecom - Equipment & Accessories": [("copper", "cost", "medium", "Copper and fibre cable inputs")],
    "Healthcare Equipment & Supplies": [("usd", "cost", "low", "Imported components and equipment")],
    "Diversified": [],
    "Paints": [("crude", "cost", "high", "Crude-derived resins and solvents"), ("other", "cost", "high", "Titanium dioxide")],
}

LEVEL_OF_SHARE = lambda s: "high" if s >= 0.15 else "medium" if s >= 0.05 else "low"

# curated company id -> NSE symbol, where names don't match automatically
SYM_OVERRIDE = {
    "tcs": "TCS", "hdfcbank": "HDFCBANK", "icicibank": "ICICIBANK", "sbi": "SBIN", "kotakbank": "KOTAKBANK",
    "mm": "M&M", "axisbank": "AXISBANK", "tatamotors": "TMPV", "ongc": "ONGC", "iocl": "IOC", "oilindia": "OIL",
    "vedanta": "VEDL", "pidilite": "PIDILITIND", "petronet": "PETRONET", "gujgas": "GUJGASLTD", "igl": "IGL",
    "apollotyre": "APOLLOTYRE", "balkrishna": "BALKRISIND", "coromandel": "COROMANDEL", "chambal": "CHAMBLFERT",
    "tatachem": "TATACHEM", "deepaknitrite": "DEEPAKNTR", "bergerpaints": "BERGEPAINT", "awl": "AWL",
    "balrampur": "BALRAMCHIN", "amararaja": "ARE&M", "welspunliving": "WELSPUNLIV", "vardhman": "VTL", "jkpaper": "JKPAPER",
    "interglobe": "INDIGO", "lt": "LT", "hul": "HINDUNILVR", "itc": "ITC", "titan": "TITAN", "asianpaints": "ASIANPAINT",
    "nestleindia": "NESTLEIND", "bhartiairtel": "BHARTIARTL", "reliance": "RELIANCE", "maruti": "MARUTI",
    "lic": "LICI", "ntpc": "NTPC", "coalindia": "COALINDIA", "godrejcp": "GODREJCP", "ambuja": "AMBUJACEM",
    "gesco": "GESHIP",
}


def load_dashboard():
    """Curated company map, exported once from Risk Radar into data/demo/curated.json."""
    d = json.load(open(os.path.join(DEMO, "curated.json"), encoding="utf-8"))
    return {k: d[k] for k in ("deps", "prod", "anchors", "lenses", "companies")}


def norm(s):
    s = s.lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"\b(ltd|limited|india|industries|company|corporation|of|the|and)\b", " ", s)
    return re.sub(r"[^a-z0-9]", "", s)


def main():
    dash = load_dashboard()
    n500 = list(csv.DictReader(open(os.path.join(DEMO, "nifty500.csv"), encoding="utf-8")))
    n200 = {r["Symbol"] for r in csv.DictReader(open(os.path.join(DEMO, "nifty200.csv"), encoding="utf-8"))}
    amfi = json.load(open(os.path.join(DEMO, "amfi_industry.json"), encoding="utf-8"))["industry"]
    funds = json.load(open(os.path.join(DEMO, "funds.json"), encoding="utf-8"))

    by_sym = {r["Symbol"]: r for r in n500}
    by_norm = {norm(r["Company Name"]): r["Symbol"] for r in n500}

    # curated company id -> symbol
    cur_sym, unmatched = {}, []
    for c in dash["companies"]:
        sym = SYM_OVERRIDE.get(c["id"])
        if not sym:
            k = norm(c["name"])
            cands = [s for n, s in by_norm.items() if k and (k == n or k in n or n in k)]
            sym = cands[0] if len(cands) == 1 else None
        if sym and sym in by_sym:
            cur_sym[c["id"]] = sym
        else:
            unmatched.append(c["id"])

    sym_cur = {v: k for k, v in cur_sym.items()}
    stocks, templ_missing = {}, set()
    for r in n500:
        sym, isin = r["Symbol"], r["ISIN Code"]
        if not sym or not isin or sym.startswith("DUMMY"):
            continue
        ind = re.sub(r"\s+", " ", amfi.get(isin, r["Industry"])).strip()
        rec = {"sym": sym, "n": r["Company Name"], "isin": isin, "ind": ind, "n200": sym in n200, "ex": []}
        cid = sym_cur.get(sym)
        if cid and (dash["deps"].get(cid) or dash["prod"].get(cid)):
            rec["basis"] = "company"
            rec["anchor"] = dash["anchors"].get(cid, "")
            agg = {}
            for com, sh in dash["deps"].get(cid, {}).items():
                d = COM_DRIVER.get(com, "other")
                agg.setdefault((d, "cost"), []).append((com, sh))
            for com, sh in dash["prod"].get(cid, {}).items():
                d = COM_DRIVER.get(com, "other")
                agg.setdefault((d, "benefit"), []).append((com, sh))
            tmpl_eff = {d: eff for d, eff, _, _ in T.get(ind, [])}
            for d in sorted({k[0] for k in agg}):
                cost, ben = agg.get((d, "cost"), []), agg.get((d, "benefit"), [])
                cs, bs = sum(x[1] for x in cost), sum(x[1] for x in ben)
                via = [x[0] for x in sorted(cost + ben, key=lambda x: -x[1])]
                if cost and ben:
                    # sells and buys the same thing: e.g. a steelmaker buying iron ore. If one side
                    # is 3x the other it dominates; otherwise it is genuinely mixed.
                    eff = "benefit" if bs >= 3 * cs else "cost" if cs >= 3 * bs else "mixed"
                    rec["ex"].append({"d": d, "e": eff, "lvl": LEVEL_OF_SHARE(max(cs, bs)), "share": round(cs, 3),
                                      "rev": round(bs, 3), "via": via})
                elif ben:
                    rec["ex"].append({"d": d, "e": "benefit", "lvl": LEVEL_OF_SHARE(bs), "rev": round(bs, 3), "via": via})
                else:
                    # refiners: crude is the main cost but margins depend on the spread to product prices
                    eff = "mixed" if tmpl_eff.get(d) == "mixed" else "cost"
                    rec["ex"].append({"d": d, "e": eff, "lvl": LEVEL_OF_SHARE(cs), "share": round(cs, 3), "via": via})
            fx = dash["lenses"].get(cid, {}).get("fx")
            if fx and fx[0] >= 3 and not any(e["d"] == "usd" for e in rec["ex"]):
                rec["ex"].append({"d": "usd", "e": "mixed", "lvl": "high" if fx[0] >= 4 else "medium", "why": fx[1]})
            # keep sector-only drivers (rates for lenders etc.) that the cost map can't express
            for d, eff, lvl, why in T.get(ind, []):
                if d in ("rates", "usd") and not any(e["d"] == d for e in rec["ex"]):
                    rec["ex"].append({"d": d, "e": eff, "lvl": lvl, "why": why, "tmpl": True})
        else:
            rec["basis"] = "sector"
            if ind not in T:
                templ_missing.add(ind)
            for d, eff, lvl, why in T.get(ind, []):
                rec["ex"].append({"d": d, "e": eff, "lvl": lvl, "why": why})
        stocks[isin] = rec

    # curated companies outside the Nifty 500 are dropped from the demo universe (logged)
    out = {
        "_meta": {
            "built": "2026-10-20",
            "universe": "Nifty 500 (NSE constituent list); Nifty 200 members flagged",
            "industry": amfi and "AMFI industry classification, from an index fund's 30 Sep 2026 portfolio",
            "basis": {
                "company": "Estimated from the company's annual report and segment disclosures (Risk Radar curated map). 'share' = share of the cost base; 'rev' = share of revenue from selling that commodity. Estimates, labelled as such.",
                "sector": "Exposures typical of the company's AMFI industry. Not company-specific: a level (high / medium / low), not a measured share.",
            },
            "not_advice": "Information only. No buy, sell or hold views, no price targets.",
        },
        "drivers": DRIVERS,
        "stocks": stocks,
        "funds": funds["funds"],
    }
    json.dump(out, open(os.path.join(DEMO, "demo.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

    n_company = sum(1 for s in stocks.values() if s["basis"] == "company")
    n200_company = sum(1 for s in stocks.values() if s["basis"] == "company" and s["n200"])
    print(f"stocks {len(stocks)} (company-basis {n_company}, of which Nifty 200: {n200_company})")
    print("curated not in Nifty 500:", unmatched)
    print("industries without a template:", sorted(templ_missing))
    for fid, f in funds["funds"].items():
        eq = [h for h in f["holdings"] if h["kind"] == "equity_in"]
        mapped = sum(h["w"] for h in eq if h["isin"] in stocks)
        comp = sum(h["w"] for h in eq if h["isin"] in stocks and stocks[h["isin"]]["basis"] == "company")
        print(f"  {fid}: Indian equity {f['indianEquityPct']}%, in universe {mapped:.1f}%, company-basis {comp:.1f}%")
    print("size", os.path.getsize(os.path.join(DEMO, "demo.json")) // 1024, "KB")


if __name__ == "__main__":
    main()
