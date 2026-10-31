# STATUS

## What was built

**gigtrack** — a local-first Python CLI for logging gig and on-call work hours,
earnings, expenses, and shift types, with weekly summaries, per-job tallies,
local JSON storage, and CSV export.

Commands:
- `gigtrack add` — log a shift (date, job, shift type, hours, rate, earnings,
  expenses, notes). Earnings default to hours × rate when omitted.
- `gigtrack list` — list all shifts with a grand total.
- `gigtrack summary` — weekly totals (hours, earnings, expenses, net) grouped by
  ISO week, plus all-time totals.
- `gigtrack jobs` — per-job tallies with average hourly rate, plus all-time
  totals.
- `gigtrack export --out FILE` — export all shifts to CSV.
- `gigtrack delete --id ID` — delete a shift by id.

Storage: local JSON file (default `~/.gigtrack/shifts.json`), overridable with
`--storage`. No accounts, no API keys, no cloud, no network. Local-first.

Files:
- `gigtrack/models.py` — Shift dataclass (id, date, job, shift_type, hours,
  rate, earnings, expenses, notes) with `net()` and dict serialization.
- `gigtrack/storage.py` — JSON read/write/add/delete.
- `gigtrack/reports.py` — weekly_summary (ISO week), job_tallies, totals.
- `gigtrack/cli.py` — argparse CLI.
- `tests/test_math.py` — earnings, net, totals, weekly, job-tally tests.
- `tests/test_dates.py` — date parsing and ISO week boundary tests.
- `pyproject.toml` — installable package with `gigtrack` console script.
- `README.md`, `LICENSE` (MIT), `.gitignore`.

## How to run it

```bash
# From the project folder (no install needed):
python3 -m gigtrack.cli add --date 2026-10-30 --job "Hospital A" \
  --type on-call --hours 12 --rate 45 --expenses 15.50
python3 -m gigtrack.cli list
python3 -m gigtrack.cli summary
python3 -m gigtrack.cli jobs
python3 -m gigtrack.cli export --out shifts.csv

# Or install:
pip install -e .
gigtrack add --date 2026-10-30 --job "Hospital A" --type on-call --hours 12 --rate 45
```

Tests:
```bash
python3 -m unittest discover -s tests -v
```

## Verification results

- `python3 -m unittest discover -s tests -v`: 15 tests, OK (7 math, 8 date).
- End-to-end smoke test passed: add two shifts, list, summary, jobs, export to
  CSV, delete — all produced correct output (verified earnings math, net
  earnings, ISO-week grouping, CSV contents).
- Python 3.13.5 used for verification. Code targets Python 3.8+ (stdlib only,
  no external dependencies).

## Known gaps

- No `__main__.py`, so `python3 -m gigtrack` does not work; use
  `python3 -m gigtrack.cli` or the installed `gigtrack` console script.
- Delete matches on exact id only (CLI help suggests first 8 chars but storage
  delete requires full id; prefix matching was not implemented).
- No per-shift edit/update command.
- Storage file path defaults to `~/.gigtrack/shifts.json`; no env-var override
  beyond `--storage`.
- No git identity configuration in repo; commits use the existing local git
  identity.
- No `.github/workflows` files (intentionally omitted per requirements).
- No secrets, API keys, or personal data in any file.

## Credit

Built by Dylan Asdale for Asdale Dynamics, LLC (Indiana, formed October 2026).
MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.
