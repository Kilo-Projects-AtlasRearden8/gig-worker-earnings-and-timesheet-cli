"""Tests for the math logic (earnings, expenses, net, totals, tallies)."""

from __future__ import annotations

import unittest

from gigtrack.models import Shift
from gigtrack.reports import job_tallies, totals, weekly_summary


def _shift(
    shift_id: str,
    date: str,
    job: str,
    shift_type: str,
    hours: float,
    rate: float,
    earnings: float,
    expenses: float,
) -> Shift:
    return Shift(
        id=shift_id,
        date=date,
        job=job,
        shift_type=shift_type,
        hours=hours,
        rate=rate,
        earnings=earnings,
        expenses=expenses,
    )


class ShiftNetTests(unittest.TestCase):
    def test_net_is_earnings_minus_expenses(self):
        shift = _shift("1", "2026-10-30", "Hospital A", "on-call", 12.0, 45.0, 540.0, 30.0)
        self.assertEqual(shift.net(), 510.0)

    def test_net_zero_when_expenses_equal_earnings(self):
        shift = _shift("2", "2026-10-30", "Hospital A", "on-call", 8.0, 40.0, 320.0, 320.0)
        self.assertEqual(shift.net(), 0.0)

    def test_net_rounds_to_cents(self):
        shift = _shift("3", "2026-10-30", "Gig Co", "gig", 5.5, 20.0, 110.0, 10.333)
        self.assertEqual(shift.net(), 99.67)


class TotalsTests(unittest.TestCase):
    def test_totals_aggregate_all_shifts(self):
        shifts = [
            _shift("1", "2026-10-30", "Job A", "gig", 10.0, 20.0, 200.0, 10.0),
            _shift("2", "2026-10-31", "Job B", "on-call", 12.0, 40.0, 480.0, 30.0),
        ]
        result = totals(shifts)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["hours"], 22.0)
        self.assertEqual(result["earnings"], 680.0)
        self.assertEqual(result["expenses"], 40.0)
        self.assertEqual(result["net"], 640.0)

    def test_totals_empty(self):
        self.assertEqual(totals([]), {"hours": 0.0, "earnings": 0.0, "expenses": 0.0, "net": 0.0, "count": 0})


class WeeklySummaryTests(unittest.TestCase):
    def test_groups_by_iso_week(self):
        shifts = [
            _shift("1", "2026-11-02", "Job A", "gig", 8.0, 20.0, 160.0, 0.0),  # Monday, week 45
            _shift("2", "2026-11-06", "Job A", "gig", 8.0, 20.0, 160.0, 0.0),  # Friday, week 45
            _shift("3", "2026-11-09", "Job A", "gig", 8.0, 20.0, 160.0, 0.0),  # Monday, week 46
        ]
        summary = weekly_summary(shifts)
        self.assertIn("2026-W45", summary)
        self.assertIn("2026-W46", summary)
        self.assertEqual(summary["2026-W45"]["count"], 2)
        self.assertEqual(summary["2026-W45"]["hours"], 16.0)
        self.assertEqual(summary["2026-W45"]["net"], 320.0)
        self.assertEqual(summary["2026-W46"]["count"], 1)

    def test_weekly_summary_empty(self):
        self.assertEqual(weekly_summary([]), {})


class JobTalliesTests(unittest.TestCase):
    def test_groups_by_job(self):
        shifts = [
            _shift("1", "2026-10-30", "Hospital A", "on-call", 12.0, 45.0, 540.0, 30.0),
            _shift("2", "2026-10-31", "Hospital A", "on-call", 8.0, 45.0, 360.0, 20.0),
            _shift("3", "2026-11-01", "Gig Co", "gig", 5.0, 25.0, 125.0, 0.0),
        ]
        tallies = job_tallies(shifts)
        self.assertEqual(tallies["Hospital A"]["count"], 2)
        self.assertEqual(tallies["Hospital A"]["hours"], 20.0)
        self.assertEqual(tallies["Hospital A"]["earnings"], 900.0)
        self.assertEqual(tallies["Hospital A"]["net"], 850.0)
        self.assertEqual(tallies["Hospital A"]["avg_rate"], 45.0)
        self.assertEqual(tallies["Gig Co"]["count"], 1)
        self.assertEqual(tallies["Gig Co"]["avg_rate"], 25.0)

    def test_job_tallies_empty(self):
        self.assertEqual(job_tallies([]), {})


if __name__ == "__main__":
    unittest.main()
