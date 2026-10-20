#!/usr/bin/env python3
"""
Parse a monthly portfolio sheet (dumped row-by-row as ' | '-joined cells) into holdings.

Input is the text of one AMC monthly portfolio disclosure sheet, read in-browser from the
AMC's own website (official source). Output is appended to data/demo/funds.json.

A holding row is any row that carries an ISIN and a % of net assets. Weights in the
disclosures are fractions (0.0775) or percents (7.75); both are normalised to percent.
Rows without an ISIN (cash, TREPS, net receivables) are summed into 'other'.

usage: parse_fund_dump.py <dump.txt> <fund_id> "<fund name>" <asof YYYY-MM-DD> <source url>
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "data", "demo", "funds.json")
ISIN = re.compile(r"^(IN[EF0-9][A-Z0-9]{9}|[A-Z]{2}[A-Z0-9]{9}[0-9])$")


def num(s):
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


SECTIONS = [  # heading keyword -> kind (order matters: first match wins)
    ("arbitrage", "arbitrage"), ("hedged", "arbitrage"),
    ("foreign", "foreign_equity"), ("overseas", "foreign_equity"),
    ("reit", "reit"), ("invit", "reit"),
    ("certificate of deposit", "debt"), ("commercial paper", "debt"), ("treasury bill", "debt"),
    ("debt", "debt"), ("bond", "debt"), ("government securit", "debt"), ("money market", "debt"),
    ("mutual fund units", "mf"), ("equity", "equity_in"),
]


def kind_of(isin, section):
    if section in ("arbitrage", "reit", "debt", "mf"):
        return section
    if isin.startswith("INF"):
        return "mf"
    if not isin.startswith("IN"):
        return "foreign_equity"
    if isin.startswith("IN0"):
        return "debt"          # government securities / T-bills
    if isin[7:9] == "01":
        return "equity_in"     # ISIN: IN + issuer type + 4-char issuer + 2-digit security type (01 = equity shares) + serial + check
    return "debt" if section != "foreign_equity" else section


def parse(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    rows = [[c.strip() for c in l.split(" | ")] for l in lines if " | " in l and "UNTRUSTED_PAGE_CONTENT" not in l]
    out, section = [], "equity_in"
    for cells in rows:
        filled = [c for c in cells if c]
        if len(filled) == 1 and not ISIN.match(filled[0]):
            h = filled[0].lower()
            if h.startswith("derivative") or h.startswith("index / stock futures"):
                break                      # derivatives block: the shorts that offset arbitrage
            for key, k in SECTIONS:
                if key in h:
                    section = k
                    break
            continue
        isin_i = next((i for i, c in enumerate(cells) if ISIN.match(c)), None)
        if isin_i is None:
            continue
        # Two layouts seen in AMC disclosures:
        #   PPFAS: code | Name | ISIN | Industry | Qty | Value | %NAV
        #   HDFC :      | ISIN | Coupon | Name | Industry | Qty | Value | %NAV
        texts_after = [c for c in cells[isin_i + 1:] if c and c != "|" and num(c) is None]
        before = cells[isin_i - 1]
        if before and before != "|" and num(before) is None:
            name, industry = before, (texts_after[0] if texts_after else "")
        else:
            name = texts_after[0] if texts_after else ""
            industry = texts_after[1] if len(texts_after) > 1 else ""
        # % to NAV: first numeric after the market value column, in (0, 1] or (0, 100]
        nums = [num(c) for c in cells[isin_i + 2:]]
        nums = [x for x in nums if x is not None]
        if len(nums) < 3:
            continue
        w = nums[2]
        if not (0 < w <= 100):
            continue
        name = re.sub(r"[\s£#*^@$~�]+$", "", name).strip()
        out.append({"isin": cells[isin_i], "name": name, "industry": industry, "w": w,
                    "kind": kind_of(cells[isin_i], section)})
    # Units differ by AMC: PPFAS reports fractions (0.0775), HDFC percents (7.75).
    # A full portfolio's listed holdings sum to ~1 as fractions or ~100 as percents.
    scale = 100.0 if sum(x["w"] for x in out) <= 1.5 else 1.0
    for x in out:
        x["w"] = round(x["w"] * scale, 3)
    return out


def main():
    path, fid, fname, asof, src = sys.argv[1:6]
    h = parse(path)
    eq = [x for x in h if x["kind"] == "equity_in"]
    mix = {}
    for x in h:
        mix[x["kind"]] = round(mix.get(x["kind"], 0) + x["w"], 2)
    data = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {"_meta": {}, "funds": {}}
    data["funds"][fid] = {"name": fname, "asof": asof, "src": src, "holdings": h,
                          "indianEquityPct": round(sum(x["w"] for x in eq), 2),
                          "totalListedPct": round(sum(x["w"] for x in h), 2), "mix": mix}
    data["_meta"] = {"note": "Monthly portfolio disclosures read from each AMC's own website. Weights are % of net assets. "
                             "Holdings without an ISIN (cash, TREPS, receivables) are not listed; the remainder to 100% is that.",
                     "built": "2026-10-20"}
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{fid}: {len(h)} holdings, Indian equity (unhedged) {data['funds'][fid]['indianEquityPct']}%, mix {mix}")
    for x in h[:5]:
        print("  ", x)


if __name__ == "__main__":
    main()
