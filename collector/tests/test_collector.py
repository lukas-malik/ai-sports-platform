"""Testy čistých funkcí sběrného skriptu. Spuštění: python -m unittest discover -s collector/tests"""

import sqlite3
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import odds_collector as oc  # noqa: E402

FIXTURE = [
    {
        "id": "evt1",
        "sport_key": "tennis_atp_us_open",
        "commence_time": "2026-09-07T20:00:00Z",
        "home_team": "Player A",
        "away_team": "Player B",
        "bookmakers": [
            {
                "key": "pinnacle",
                "title": "Pinnacle",
                "last_update": "2026-09-07T17:55:00Z",
                "markets": [
                    {
                        "key": "h2h",
                        "last_update": "2026-09-07T17:56:00Z",
                        "outcomes": [
                            {"name": "Player A", "price": 1.62},
                            {"name": "Player B", "price": 2.45},
                        ],
                    }
                ],
            },
            {
                "key": "betano",
                "title": "Betano",
                "markets": [
                    {"key": "h2h", "outcomes": [{"name": "Player A", "price": 1.55}, {"name": "Player B"}]}
                ],
            },
        ],
    }
]


class FlattenTests(unittest.TestCase):
    def test_flatten_produces_one_row_per_outcome_with_price(self):
        rows = oc.flatten_odds("tennis_atp_us_open", "2026-09-07T18:00:00Z", FIXTURE)
        self.assertEqual(len(rows), 3)
        pin = [r for r in rows if r.bookmaker_key == "pinnacle"]
        self.assertEqual({r.outcome_name: r.price for r in pin}, {"Player A": 1.62, "Player B": 2.45})
        self.assertEqual(pin[0].bookmaker_last_update, "2026-09-07T17:56:00Z")
        bet = [r for r in rows if r.bookmaker_key == "betano"]
        self.assertEqual(len(bet), 1)
        self.assertIsNone(bet[0].bookmaker_last_update)


class BudgetTests(unittest.TestCase):
    def test_daily_allowance_spreads_remaining_minus_reserve(self):
        now = datetime(2026, 9, 7, tzinfo=timezone.utc)  # 24 dní do konce měsíce včetně dneška
        self.assertEqual(oc.days_left_in_month(now), 24)
        self.assertEqual(oc.daily_allowance(500, now), (500 - oc.MONTHLY_RESERVE) // 24)
        self.assertEqual(oc.daily_allowance(None, now), 0)
        self.assertEqual(oc.daily_allowance(10, now), 0)

    def test_days_left_december(self):
        self.assertEqual(oc.days_left_in_month(datetime(2026, 12, 31, tzinfo=timezone.utc)), 1)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.executescript(oc.SCHEMA)

    def test_store_and_prioritize(self):
        ts1 = "2026-09-07T15:00:00Z"
        rows = oc.flatten_odds("tennis_atp_us_open", ts1, FIXTURE)
        self.conn.execute("INSERT INTO runs (ts_utc, credits_used) VALUES (?, 1)", (ts1,))
        oc.store_snapshot(self.conn, 1, "tennis_atp_us_open", "US Open", ts1, FIXTURE, rows)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM odds").fetchone()[0], 3)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM events").fetchone()[0], 1)

        now = datetime(2026, 9, 7, 18, 30, tzinfo=timezone.utc)  # 90 minut před startem zápasu
        self.assertTrue(oc.next_commence_within(self.conn, "tennis_atp_us_open", now, oc.CLOSING_WINDOW_MINUTES))
        # Poslední snapshot je 210 minut starý, snapshot se má udělat.
        self.assertTrue(oc.should_snapshot(self.conn, "tennis_atp_us_open", now))
        # Turnaj bez záznamu jde na konec (nemá closing prioritu), ale je nejstarší, takže mezi neprioritními první.
        order = oc.prioritize(self.conn, ["tennis_wta_new", "tennis_atp_us_open"], now)
        self.assertEqual(order[0], "tennis_atp_us_open")
        self.assertEqual(oc.credits_used_today(self.conn, now), 1)

    def test_should_snapshot_respects_min_gap(self):
        ts1 = "2026-09-07T15:00:00Z"
        self.conn.execute("INSERT INTO runs (ts_utc, credits_used) VALUES (?, 1)", (ts1,))
        self.conn.execute("INSERT INTO sport_snapshots VALUES (?, ?, 1, 0)", ("tennis_x", ts1))
        now = datetime(2026, 9, 7, 15, 45, tzinfo=timezone.utc)
        self.assertFalse(oc.should_snapshot(self.conn, "tennis_x", now))


if __name__ == "__main__":
    unittest.main()
