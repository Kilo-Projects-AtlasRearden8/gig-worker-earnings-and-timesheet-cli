"""Reports: weekly summaries and per-job tallies."""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Iterable

from .models import Shift


def _week_key(shift: Shift) -> str:
    """ISO calendar week key 'YYYY-WNN' (Monday-start week)."""
    year, week, _weekday = date.fromisoformat(shift.date).isocalendar()
    return f"{year}-W{week:02d}"


def weekly_summary(shifts: Iterable[Shift]) -> dict[str, dict]:
    """Aggregate shifts by ISO week.

    Returns a dict keyed by 'YYYY-WNN' with hours, earnings, expenses, net,
    shift count, and the list of shift ids in that week.
    """
    grouped: dict[str, list[Shift]] = defaultdict(list)
    for shift in shifts:
        grouped[_week_key(shift)].append(shift)

    summary: dict[str, dict] = {}
    for week_key in sorted(grouped):
        week_shifts = grouped[week_key]
        hours = round(sum(s.hours for s in week_shifts), 2)
        earnings = round(sum(s.earnings for s in week_shifts), 2)
        expenses = round(sum(s.expenses for s in week_shifts), 2)
        summary[week_key] = {
            "week": week_key,
            "hours": hours,
            "earnings": earnings,
            "expenses": expenses,
            "net": round(earnings - expenses, 2),
            "count": len(week_shifts),
            "ids": [s.id for s in week_shifts],
        }
    return summary


def job_tallies(shifts: Iterable[Shift]) -> dict[str, dict]:
    """Aggregate shifts by job name."""
    grouped: dict[str, list[Shift]] = defaultdict(list)
    for shift in shifts:
        grouped[shift.job].append(shift)

    tallies: dict[str, dict] = {}
    for job in sorted(grouped):
        job_shifts = grouped[job]
        hours = round(sum(s.hours for s in job_shifts), 2)
        earnings = round(sum(s.earnings for s in job_shifts), 2)
        expenses = round(sum(s.expenses for s in job_shifts), 2)
        tallies[job] = {
            "job": job,
            "hours": hours,
            "earnings": earnings,
            "expenses": expenses,
            "net": round(earnings - expenses, 2),
            "count": len(job_shifts),
            "avg_rate": round(earnings / hours, 2) if hours else 0.0,
        }
    return tallies


def totals(shifts: Iterable[Shift]) -> dict:
    """Grand totals across all shifts."""
    shift_list = list(shifts)
    hours = round(sum(s.hours for s in shift_list), 2)
    earnings = round(sum(s.earnings for s in shift_list), 2)
    expenses = round(sum(s.expenses for s in shift_list), 2)
    return {
        "hours": hours,
        "earnings": earnings,
        "expenses": expenses,
        "net": round(earnings - expenses, 2),
        "count": len(shift_list),
    }
