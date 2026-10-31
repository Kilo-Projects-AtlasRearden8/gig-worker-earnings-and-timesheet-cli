"""Command-line interface for the gig worker earnings and timesheet CLI."""

from __future__ import annotations

import argparse
import csv
import sys
import uuid
from datetime import date
from typing import Optional, Sequence

from .models import Shift
from .reports import job_tallies, totals, weekly_summary
from .storage import DEFAULT_STORAGE_PATH, Storage


def _parse_date(value: str) -> str:
    """Validate and normalize a date string to ISO YYYY-MM-DD."""
    parsed = date.fromisoformat(value)
    return parsed.isoformat()


def _money(value: str) -> float:
    return round(float(value), 2)


def _new_shift(
    date_str: str,
    job: str,
    shift_type: str,
    hours: float,
    rate: float,
    earnings: Optional[float],
    expenses: float,
    notes: str,
) -> Shift:
    if earnings is None:
        earnings = round(hours * rate, 2)
    return Shift(
        id=str(uuid.uuid4()),
        date=date_str,
        job=job,
        shift_type=shift_type,
        hours=hours,
        rate=rate,
        earnings=earnings,
        expenses=expenses,
        notes=notes,
    )


def cmd_add(args: argparse.Namespace) -> int:
    storage = Storage(args.storage)
    date_str = _parse_date(args.date)
    shift = _new_shift(
        date_str=date_str,
        job=args.job,
        shift_type=args.type,
        hours=args.hours,
        rate=args.rate,
        earnings=args.earnings,
        expenses=args.expenses,
        notes=args.notes,
    )
    storage.add(shift)
    print(f"Added shift {shift.id[:8]}: {shift.date} | {shift.job} | {shift.shift_type} | {shift.hours}h | ${shift.earnings:.2f}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    storage = Storage(args.storage)
    shifts = storage.load()
    if not shifts:
        print("No shifts recorded.")
        return 0
    for shift in shifts:
        print(
            f"{shift.id[:8]}  {shift.date}  {shift.job:<20} {shift.shift_type:<12} "
            f"{shift.hours:>5}h  ${shift.rate:>6.2f}/hr  ${shift.earnings:>8.2f}  "
            f"${shift.expenses:>7.2f}  net ${shift.net():>7.2f}"
        )
    grand = totals(shifts)
    print(
        f"--- total: {grand['count']} shifts, {grand['hours']}h, "
        f"${grand['earnings']:.2f} earned, ${grand['expenses']:.2f} expenses, "
        f"${grand['net']:.2f} net"
    )
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    storage = Storage(args.storage)
    shifts = storage.load()
    summary = weekly_summary(shifts)
    if not summary:
        print("No shifts recorded.")
        return 0
    for week_key, week in summary.items():
        print(
            f"{week_key}: {week['count']} shift(s), {week['hours']}h, "
            f"${week['earnings']:.2f} earned, ${week['expenses']:.2f} expenses, "
            f"${week['net']:.2f} net"
        )
    grand = totals(shifts)
    print(
        f"--- all time: {grand['count']} shifts, {grand['hours']}h, "
        f"${grand['earnings']:.2f} earned, ${grand['expenses']:.2f} expenses, "
        f"${grand['net']:.2f} net"
    )
    return 0


def cmd_jobs(args: argparse.Namespace) -> int:
    storage = Storage(args.storage)
    shifts = storage.load()
    tallies = job_tallies(shifts)
    if not tallies:
        print("No shifts recorded.")
        return 0
    for job, tally in tallies.items():
        print(
            f"{tally['job']:<20} {tally['count']:>2} shift(s), {tally['hours']:>5}h, "
            f"${tally['earnings']:>9.2f} earned, ${tally['expenses']:>8.2f} expenses, "
            f"${tally['net']:>9.2f} net (avg ${tally['avg_rate']:.2f}/hr)"
        )
    grand = totals(shifts)
    print(
        f"--- all time: {grand['count']} shifts, {grand['hours']}h, "
        f"${grand['earnings']:.2f} earned, ${grand['expenses']:.2f} expenses, "
        f"${grand['net']:.2f} net"
    )
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    storage = Storage(args.storage)
    shifts = storage.load()
    out_path = args.out
    with open(out_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["id", "date", "job", "shift_type", "hours", "rate", "earnings", "expenses", "net", "notes"]
        )
        for shift in shifts:
            writer.writerow(
                [
                    shift.id,
                    shift.date,
                    shift.job,
                    shift.shift_type,
                    shift.hours,
                    shift.rate,
                    shift.earnings,
                    shift.expenses,
                    shift.net(),
                    shift.notes,
                ]
            )
    print(f"Exported {len(shifts)} shift(s) to {out_path}")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    storage = Storage(args.storage)
    if storage.delete(args.id):
        print(f"Deleted shift {args.id[:8]}")
        return 0
    print(f"Shift {args.id[:8]} not found.")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gigtrack",
        description="Log gig and on-call work hours, earnings, expenses, and shift types.",
    )
    parser.add_argument(
        "--storage",
        default=DEFAULT_STORAGE_PATH,
        help=f"Path to the local JSON storage file (default: {DEFAULT_STORAGE_PATH})",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new shift")
    p_add.add_argument("--date", required=True, help="Shift date (YYYY-MM-DD)")
    p_add.add_argument("--job", required=True, help="Employer or gig name")
    p_add.add_argument("--type", required=True, help="Shift type (e.g. gig, on-call, per-diem, contract)")
    p_add.add_argument("--hours", required=True, type=float, help="Hours worked")
    p_add.add_argument("--rate", required=True, type=float, help="Hourly rate")
    p_add.add_argument("--earnings", type=float, default=None, help="Total earnings (defaults to hours * rate)")
    p_add.add_argument("--expenses", type=_money, default=0.0, help="Expenses for the shift")
    p_add.add_argument("--notes", default="", help="Notes")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List all shifts")
    p_list.set_defaults(func=cmd_list)

    p_summary = sub.add_parser("summary", help="Print weekly summaries")
    p_summary.set_defaults(func=cmd_summary)

    p_jobs = sub.add_parser("jobs", help="Print per-job tallies")
    p_jobs.set_defaults(func=cmd_jobs)

    p_export = sub.add_parser("export", help="Export shifts to CSV")
    p_export.add_argument("--out", required=True, help="Output CSV path")
    p_export.set_defaults(func=cmd_export)

    p_delete = sub.add_parser("delete", help="Delete a shift by id")
    p_delete.add_argument("--id", required=True, help="Shift id (full or first 8 chars)")
    p_delete.set_defaults(func=cmd_delete)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
