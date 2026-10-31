"""Tests for the date logic (parsing, ISO week grouping, week boundaries)."""

from __future__ import annotations

import unittest
from datetime import date

from gigtrack.cli import _parse_date
from gigtrack.models import Shift
from gigtrack.reports import weekly_summary


class DateParsingTests(unittest.TestCase):
    def test_valid_iso_date_normalized(self):
        self.assertEqual(_parse_date("2026-10-30"), "2026-10-30")

    def test_padded_month_and_day(self):
        self.assertEqual(_parse_date("2026-01-05"), "2026-01-05")

    def test_invalid_date_raises(self):
        with self.assertRaises(ValueError):
            _parse_date("2026-13-01")
        with self.assertRaises(ValueError):
            _parse_date("not-a-date")
        with self.assertRaises(ValueError):
            _parse_date("10/30/2026")
        with self.assertRaises(ValueError):
            _parse_date("2026-1-5")


class WeekBoundaryTests(unittest.TestCase):
    def test_week_starts_on_monday(self):
        # Sunday Nov 1 2026 belongs to ISO week 44 of 2026 (Mon Oct 26 - Sun Nov 1)
        sunday = Shift("1", "2026-11-01", "J", "gig", 8.0, 20.0, 160.0, 0.0)
        # Monday Nov 2 2026 starts ISO week 45
        monday = Shift("2", "2026-11-02", "J", "gig", 8.0, 20.0, 160.0, 0.0)
        summary = weekly_summary([sunday, monday])
        self.assertEqual(summary["2026-W44"]["count"], 1)
        self.assertEqual(summary["2026-W45"]["count"], 1)

    def test_year_rollover_week(self):
        # Wednesday Dec 30 2026 falls in ISO week 53 of 2026
        shift = Shift("1", "2026-12-30", "J", "gig", 8.0, 20.0, 160.0, 0.0)
        summary = weekly_summary([shift])
        self.assertEqual(summary["2026-W53"]["count"], 1)

    def test_date_is_stored_iso(self):
        shift = Shift("1", "2026-10-30", "J", "gig", 8.0, 20.0, 160.0, 0.0)
        self.assertEqual(shift.date, "2026-10-30")
        self.assertEqual(date.fromisoformat(shift.date), date(2026, 10, 30))


if __name__ == "__main__":
    unittest.main()
