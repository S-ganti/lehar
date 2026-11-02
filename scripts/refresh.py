#!/usr/bin/env python3
"""
Lehar daily data refresh. Python 3.10+ standard library only.

Fetches the price series behind Lehar's factors, keeps their history in
data/series/ (so a feed outage leaves slightly stale data rather than none),
and writes data/latest.json: the latest move per series, its usual size, the
price level, and the events worth a card on the page.

Sources (free, no keys), adapted from the Risk Radar pipeline:
  fred.stlouisfed.org   keyless fredgraph.csv
      daily (EIA):     Brent DCOILBRENTEU, Henry Hub DHHNGSP
      monthly (IMF):   copper, aluminium, iron ore, thermal coal, palm oil,
                       rubber, sugar, wheat, cocoa
  api.frankfurter.dev   ECB daily reference rates (USD/INR)
  query1.finance.yahoo  COMEX gold front month (GC=F), daily

An event is any of: a move at least EVENT_Z times the series' usual swing over
the same window; a level at least LEVEL_Z usual swings away from its average of
the past year; or a close at the highest or lowest level in the history kept.
Events are facts about prices. What they mean for a portfolio is worked out in
the browser from the user's own holdings.

Run:  python scripts/refresh.py
"""
import csv
import io
import json
import math
import os
import statistics
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
SERIES_DIR = os.path.join(DATA_DIR, "series")
UA = {"User-Agent": "Mozilla/5.0 (lehar-refresh; +https://github.com/S-ganti/lehar)"}
HISTORY_YEARS = 5.3

EVENT_Z = 1.5          # a move this many times its usual swing is an event
LEVEL_Z = 3.0          # a level this many usual swings from its one-year average is an event
EXTREME_MIN_YEARS = 3  # need this much history before calling a high or low
FRESH_DAYS = {"D": 10, "M": 75}  # older data never makes an event card

SOURCES = {
    "crude":   {"kind": "fred",  "id": "DCOILBRENTEU", "freq": "D", "label": "Brent (EIA via FRED)", "unit": "USD/bbl"},
    "natgas":  {"kind": "fred",  "id": "DHHNGSP",      "freq": "D", "label": "Henry Hub (EIA via FRED)", "unit": "USD/MMBtu"},
    "gold":    {"kind": "yahoo", "id": "GC=F",         "freq": "D", "label": "COMEX gold front month (Yahoo)", "unit": "USD/oz"},
    "usdinr":  {"kind": "ecb",   "id": "INR",          "freq": "D", "label": "USD/INR (ECB via Frankfurter)", "unit": "₹ per USD"},
    "copper":  {"kind": "fred",  "id": "PCOPPUSDM",    "freq": "M", "label": "Copper (IMF via FRED)", "unit": "USD/t"},
    "alum":    {"kind": "fred",  "id": "PALUMUSDM",    "freq": "M", "label": "Aluminium (IMF via FRED)", "unit": "USD/t"},
    "ironore": {"kind": "fred",  "id": "PIORECRUSDM",  "freq": "M", "label": "Iron ore (IMF via FRED)", "unit": "USD/dmt"},
    "coal":    {"kind": "fred",  "id": "PCOALAUUSDM",  "freq": "M", "label": "Australian thermal coal (IMF via FRED)", "unit": "USD/t"},
    "palm":    {"kind": "fred",  "id": "PPOILUSDM",    "freq": "M", "label": "Palm oil (IMF via FRED)", "unit": "USD/t"},
    "natrub":  {"kind": "fred",  "id": "PRUBBUSDM",    "freq": "M", "label": "Rubber (IMF via FRED)", "unit": "US cents/lb"},
    "sugar":   {"kind": "fred",  "id": "PSUGAISAUSDM", "freq": "M", "label": "Sugar (IMF via FRED)", "unit": "US cents/lb"},
    "wheat":   {"kind": "fred",  "id": "PWHEAMTUSDM",  "freq": "M", "label": "Wheat (IMF via FRED)", "unit": "USD/t"},
    "cocoa":   {"kind": "fred",  "id": "PCOCOUSDM",    "freq": "M", "label": "Cocoa (IMF via FRED)", "unit": "USD/t"},
}


# ---------------------------------------------------------------- fetching --
def http_get(url, timeout=45, retries=2):
    last = None
    for _ in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - each source degrades on its own
            last = e
    print(f"  ! fetch failed: {url} ({last})", file=sys.stderr)
    return None


def cutoff(today):
    return (today - timedelta(days=int(HISTORY_YEARS * 365))).isoformat()


def fetch_fred(series_id, today):
    raw = http_get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}")
    if not raw:
        return []
    rows, cut = [], cutoff(today)
    for rec in csv.reader(io.StringIO(raw.decode("utf-8", "replace"))):
        if len(rec) != 2 or rec[0] in ("DATE", "observation_date"):
            continue
        d, v = rec
        if d >= cut and v not in (".", ""):
            try:
                rows.append((d, float(v)))
            except ValueError:
                continue
    return rows


def fetch_ecb(ccy, today):
    raw = http_get(f"https://api.frankfurter.dev/v1/{cutoff(today)}..{today.isoformat()}?base=USD&symbols={ccy}", timeout=60)
    try:
        rates = json.loads(raw.decode("utf-8"))["rates"]
    except Exception:  # noqa: BLE001
        return []
    return sorted((d, float(r[ccy])) for d, r in rates.items() if ccy in r)


def fetch_yahoo(symbol, today):
    raw = http_get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5y&interval=1d", timeout=60)
    try:
        res = json.loads(raw.decode("utf-8"))["chart"]["result"][0]
        stamps, closes = res["timestamp"], res["indicators"]["quote"][0]["close"]
    except Exception:  # noqa: BLE001
        return []
    cut, rows = cutoff(today), {}
    for ts, c in zip(stamps, closes):
        if c is not None:
            d = datetime.fromtimestamp(ts, timezone.utc).date().isoformat()
            if d >= cut:
                rows[d] = round(float(c), 2)
    return sorted(rows.items())


def fetch(cid, today):
    s = SOURCES[cid]
    if s["kind"] == "fred":
        return fetch_fred(s["id"], today)
    if s["kind"] == "ecb":
        return fetch_ecb(s["id"], today)
    return fetch_yahoo(s["id"], today)


def merge_series(cid, fetched, today):
    """Union of the committed history and this run's fetch, trimmed to the window."""
    path = os.path.join(SERIES_DIR, f"{cid}.json")
    try:
        with open(path, encoding="utf-8") as f:
            merged = {d: float(v) for d, v in json.load(f)}
    except Exception:  # noqa: BLE001
        merged = {}
    n_old = len(merged)
    merged.update(dict(fetched or []))
    cut = cutoff(today)
    rows = sorted((d, v) for d, v in merged.items() if d >= cut)
    if rows:
        os.makedirs(SERIES_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rows, f, separators=(",", ":"))
    return rows, n_old


# ------------------------------------------------------------------- maths --
def log_returns(vals):
    return [math.log(b / a) for a, b in zip(vals, vals[1:]) if a > 0 and b > 0]


def ewma_sigmas(rets, lam=0.94, seed=30):
    """RiskMetrics EWMA daily sigma, one per return after the seed window."""
    if len(rets) < seed + 5:
        return []
    var = sum(r * r for r in rets[:seed]) / seed
    out = []
    for r in rets[seed:]:
        var = lam * var + (1 - lam) * r * r
        out.append(math.sqrt(var))
    return out


def rolling_std(rets, window=36):
    out = []
    for i in range(window, len(rets) + 1):
        out.append(statistics.stdev(rets[i - window:i]))
    return out


def years_between(d0, d1):
    return (date.fromisoformat(d1) - date.fromisoformat(d0)).days / 365.25


def analyse(rows, freq):
    """Move, usual swing, level and event flags for one series.

    rows: [(iso date, value)] ascending. Daily series move over 20 trading
    days; monthly series over one month. The usual swing is the median of the
    series' own volatility over all the history kept (about five years), in log
    terms over the same window, so a crisis year does not become the baseline.
    """
    vals = [v for _, v in rows]
    rets = log_returns(vals)
    n = 20 if freq == "D" else 1
    if len(vals) <= n + 40:
        return None
    lr = math.log(vals[-1] / vals[-1 - n])
    if freq == "D":
        sig = ewma_sigmas(rets)
        if not sig:
            return None
        usual = statistics.median(s * math.sqrt(n) for s in sig)
        vol_month = sig[-1] * math.sqrt(21)
    else:
        sig = rolling_std(rets)
        if not sig:
            return None
        usual = statistics.median(sig)
        vol_month = sig[-1]
    z = abs(lr) / usual if usual > 0 else 0.0
    year = vals[-252:] if freq == "D" else vals[-12:]
    avg = sum(year) / len(year)
    z_level = abs(math.log(vals[-1] / avg)) / usual if usual > 0 else 0.0
    span = years_between(rows[0][0], rows[-1][0])
    hist = vals[:-1]
    extreme = None
    if span >= EXTREME_MIN_YEARS and hist:
        if vals[-1] > max(hist):
            extreme = "high"
        elif vals[-1] < min(hist):
            extreme = "low"
    return {
        "move": round((math.exp(lr) - 1) * 100, 2),
        "usual": round((math.exp(usual) - 1) * 100, 2),
        "z": round(z, 2),
        "z_level": round(z_level, 2),
        "avg_1y": round(avg, 2),
        "vs_avg": round((vals[-1] / avg - 1) * 100, 2),
        "from": {"date": rows[-1 - n][0], "v": round(vals[-1 - n], 2)},
        "to": {"date": rows[-1][0], "v": round(vals[-1], 2)},
        "extreme": extreme,
        "span_years": int(span),
        "vol_month": round(vol_month, 4),
        "n": len(rets),
    }


def is_event(a, freq, asof, today):
    if not a:
        return False
    fresh = (today - date.fromisoformat(asof)).days <= FRESH_DAYS[freq]
    return fresh and bool(event_kinds(a))


def event_kinds(a):
    kinds = []
    if a["z"] >= EVENT_Z:
        kinds.append("move")
    if a["z_level"] >= LEVEL_Z:
        kinds.append("level")
    if a["extreme"]:
        kinds.append(a["extreme"])
    return kinds


def severity(e):
    return max(e["z"], e["z_level"] / 2) + (1 if e["extreme"] else 0)


# -------------------------------------------------------------------- main --
def main(today=None):
    today = today or date.today()
    out_moves, out_vols, levels, events, degraded = {}, {}, {}, [], []
    for cid, s in SOURCES.items():
        fetched = fetch(cid, today)
        rows, n_old = merge_series(cid, fetched, today)
        if not fetched:
            degraded.append({"series": cid, "source": s["label"],
                             "using_persisted_to": rows[-1][0] if rows else None})
        a = analyse(rows, s["freq"]) if rows else None
        if not a:
            print(f"  {cid:8s} skipped ({len(rows)} rows)")
            continue
        asof = a["to"]["date"]
        out_moves[cid] = a["move"]
        out_vols[cid] = {"freq": s["freq"], "monthly": a["vol_month"], "asof": asof, "n": a["n"],
                         "src": s["label"], "method": "EWMA(0.94) daily" if s["freq"] == "D" else "rolling 36m std of monthly returns"}
        levels[cid] = {"v": a["to"]["v"], "asof": asof, "from": a["from"], "unit": s["unit"], "usual": a["usual"],
                       "z": a["z"], "avg_1y": a["avg_1y"], "vs_avg": a["vs_avg"], "z_level": a["z_level"]}
        flag = ""
        if is_event(a, s["freq"], asof, today):
            events.append({"series": cid, "freq": s["freq"], "kinds": event_kinds(a), "move": a["move"], "usual": a["usual"],
                           "z": a["z"], "z_level": a["z_level"], "avg_1y": a["avg_1y"], "vs_avg": a["vs_avg"],
                           "extreme": a["extreme"], "span_years": a["span_years"], "from": a["from"], "to": a["to"],
                           "unit": s["unit"], "src": s["label"]})
            flag = "  EVENT"
        print(f"  {cid:8s} {s['freq']} {len(rows):5d} rows  {asof} = {a['to']['v']}  move {a['move']:+.1f}%  "
              f"usual {a['usual']:.1f}%  z {a['z']:.1f}  vs 1y avg {a['vs_avg']:+.1f}% (z {a['z_level']:.1f}){'  ' + a['extreme'] if a['extreme'] else ''}"
              f"{'  [persisted]' if not fetched else ''}{flag}")
    events.sort(key=lambda e: -severity(e))
    latest = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "moves": out_moves,
        "vols": out_vols,
        "levels": levels,
        "events": events,
        "degraded_sources": degraded,
        "notes": [
            "Daily series move over 20 trading days; monthly series (IMF) month over month.",
            f"An event is a move at least {EVENT_Z}x the series' usual swing over the same window, "
            f"a level at least {LEVEL_Z}x that swing away from its one-year average, "
            "or a close at the highest or lowest level in the history kept here. "
            "The usual swing is the median volatility over all the history kept (about five years).",
            "Price history is kept in data/series/ and merged each run; a series running on kept data is listed in degraded_sources.",
        ],
    }
    if len(out_moves) < len(SOURCES) // 2:
        print(f"Only {len(out_moves)} series computed; leaving data/latest.json unchanged.", file=sys.stderr)
        return 1
    with open(os.path.join(DATA_DIR, "latest.json"), "w", encoding="utf-8") as f:
        json.dump(latest, f, indent=1, ensure_ascii=False)
    print(f"\nWrote data/latest.json: {len(out_moves)} series, {len(events)} events, {len(degraded)} on kept data")
    return 0


if __name__ == "__main__":
    sys.exit(main())
