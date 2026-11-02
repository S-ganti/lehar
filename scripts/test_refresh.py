#!/usr/bin/env python3
"""Checks for scripts/refresh.py. Run: python scripts/test_refresh.py"""
import json
import math
import os
import random
import sys
import unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refresh as R  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def walk(n, sigma, seed=1, start=100.0, end=date(2026, 10, 30), freq="D"):
    """A random walk of n points ending on `end`, daily (weekdays) or monthly."""
    rng = random.Random(seed)
    v, vals = start, []
    for _ in range(n):
        v *= math.exp(rng.gauss(0, sigma))
        vals.append(round(v, 4))
    if freq == "D":
        days, d = [], end
        while len(days) < n:
            if d.weekday() < 5:
                days.append(d.isoformat())
            d -= timedelta(days=1)
        days.reverse()
    else:
        y, m, days = end.year, end.month, []
        for _ in range(n):
            days.append(date(y, m, 1).isoformat())
            m -= 1
            if m == 0:
                y, m = y - 1, 12
        days.reverse()
    return list(zip(days, vals))


class Analyse(unittest.TestCase):
    def test_calm_series_has_no_event(self):
        rows = walk(1300, 0.01, seed=3)
        # pin today and 20 days ago to the year's average: no move, no stretched level, no new high or low
        avg = sum(v for _, v in rows[-252:]) / 252
        rows[-1] = (rows[-1][0], avg)
        rows[-21] = (rows[-21][0], avg)
        a = R.analyse(rows, "D")
        self.assertIsNotNone(a)
        self.assertIsNone(a["extreme"])
        self.assertEqual(R.event_kinds(a), [])

    def test_jump_is_a_move_event(self):
        rows = walk(1300, 0.01, seed=5)
        d, v = rows[-1]
        rows[-1] = (d, v * 1.25)  # +25% against a usual 20-day swing of about 4.5%
        a = R.analyse(rows, "D")
        self.assertIn("move", R.event_kinds(a))
        self.assertGreater(a["z"], R.EVENT_Z)
        self.assertAlmostEqual(a["move"], (rows[-1][1] / rows[-21][1] - 1) * 100, places=1)

    def test_new_high_is_flagged(self):
        rows = walk(1300, 0.01, seed=7)
        top = max(v for _, v in rows)
        rows[-1] = (rows[-1][0], top * 1.001)
        a = R.analyse(rows, "D")
        self.assertEqual(a["extreme"], "high")
        self.assertIn("high", R.event_kinds(a))

    def test_short_history_never_calls_a_high(self):
        rows = walk(400, 0.01, seed=7)  # about 1.6 years
        rows[-1] = (rows[-1][0], max(v for _, v in rows) * 1.01)
        a = R.analyse(rows, "D")
        self.assertIsNone(a["extreme"])

    def test_stretched_level_is_an_event(self):
        rows = walk(1300, 0.005, seed=9)
        # step the last 25 days up 30%: the 20-day move is small, the level is far from the year's average
        rows = rows[:-25] + [(d, v * 1.30) for d, v in rows[-25:]]
        a = R.analyse(rows, "D")
        self.assertIn("level", R.event_kinds(a))
        self.assertGreater(a["vs_avg"], 15)

    def test_monthly_series(self):
        rows = walk(62, 0.05, seed=11, freq="M")
        a = R.analyse(rows, "M")
        self.assertIsNotNone(a)
        self.assertAlmostEqual(a["move"], (rows[-1][1] / rows[-2][1] - 1) * 100, places=1)

    def test_stale_data_is_not_an_event(self):
        rows = walk(1300, 0.01, seed=5)
        rows[-1] = (rows[-1][0], rows[-1][1] * 1.25)
        a = R.analyse(rows, "D")
        asof = rows[-1][0]
        self.assertTrue(R.is_event(a, "D", asof, date.fromisoformat(asof) + timedelta(days=3)))
        self.assertFalse(R.is_event(a, "D", asof, date.fromisoformat(asof) + timedelta(days=30)))

    def test_too_short_returns_none(self):
        self.assertIsNone(R.analyse(walk(30, 0.01), "D"))


class LatestJson(unittest.TestCase):
    """The committed data/latest.json has what index.html reads."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(ROOT, "data", "latest.json"), encoding="utf-8") as f:
            cls.L = json.load(f)
        with open(os.path.join(ROOT, "data", "demo", "demo.json"), encoding="utf-8") as f:
            cls.D = json.load(f)

    def test_keys(self):
        for k in ("generated", "moves", "vols", "levels", "events", "degraded_sources"):
            self.assertIn(k, self.L)

    def test_every_factor_series_is_covered(self):
        wanted = {d["series"] for d in self.D["drivers"].values() if d.get("series")}
        self.assertEqual(wanted - set(R.SOURCES), set(), "a factor points at a series refresh.py does not fetch")
        self.assertGreaterEqual(len(set(self.L["moves"]) & wanted), len(wanted) - 2, "most factor series should have data")

    def test_series_records(self):
        for sr, vo in self.L["vols"].items():
            self.assertIn(vo["freq"], ("D", "M"))
            date.fromisoformat(vo["asof"])
            self.assertIn(sr, self.L["moves"])
            lv = self.L["levels"][sr]
            for k in ("v", "asof", "unit", "usual", "z", "avg_1y", "vs_avg"):
                self.assertIn(k, lv)

    def test_events(self):
        for e in self.L["events"]:
            self.assertIn(e["series"], R.SOURCES)
            self.assertTrue(e["kinds"])
            for k in ("move", "usual", "z", "z_level", "avg_1y", "vs_avg", "from", "to", "unit", "src", "freq"):
                self.assertIn(k, e)


if __name__ == "__main__":
    unittest.main(verbosity=1)
