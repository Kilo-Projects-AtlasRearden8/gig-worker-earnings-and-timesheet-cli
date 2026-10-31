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
- `gigtrack delete --id ID` — delete a shift by full ID or unambiguous prefix.

Storage: local JSON file (default `~/.gigtrack/shifts.json`), overridable with
`--storage` or the `GIGTRACK_STORAGE` environment variable. No accounts, no API
keys, no cloud, no network. Local-first.

Files:
- `gigtrack/__init__.py` — package marker and version.
- `gigtrack/__main__.py` — enables `python3 -m gigtrack`.
- `gigtrack/cli.py` — argparse CLI with add/list/summary/jobs/export/delete.
- `gigtrack/models.py` — Shift dataclass with `net()` and dict serialization.
- `gigtrack/reports.py` — weekly_summary (ISO week), job_tallies, totals.
- `gigtrack/storage.py` — JSON read/write/add/delete with prefix delete.
- `tests/test_math.py` — earnings, net, totals, weekly, job-tally tests.
- `tests/test_dates.py` — date parsing and ISO week boundary tests.
- `tests/test_storage.py` — delete (exact, prefix, ambiguous, nonexistent) and
  env-var storage path tests.
- `pyproject.toml` — installable package with `gigtrack` console script.
- `README.md`, `LICENSE` (MIT), `.gitignore`, `STATUS.md`.

## How to run it

```bash
# From the project folder (no install needed):
python3 -m gigtrack add --date 2026-10-30 --job "Hospital A" \
  --type on-call --hours 12 --rate 45 --expenses 15.50
python3 -m gigtrack list
python3 -m gigtrack summary
python3 -m gigtrack jobs
python3 -m gigtrack export --out shifts.csv

# Or install:
pip install -e .
gigtrack add --date 2026-10-30 --job "Hospital A" --type on-call --hours 12 --rate 45

# Use a different storage file:
gigtrack --storage /path/to/my-shifts.json list
# or:
export GIGTRACK_STORAGE="/path/to/my-shifts.json"
gigtrack list
```

Tests:
```bash
python3 -m unittest discover -s tests -v
```

## Verification results

- `python3 -m unittest discover -s tests -v`: 20 tests, OK (7 math, 8 date,
  5 storage).
- End-to-end smoke test passed: add two shifts, list, summary, jobs, export to
  CSV, delete by prefix — all produced correct output (verified earnings math,
  net earnings, ISO-week grouping, CSV contents, prefix delete).
- `python3 -m gigtrack` (via `__main__.py`) works correctly.
- `GIGTRACK_STORAGE` environment variable override works.
- Python 3.13.5 used for verification. Code targets Python 3.8+ (stdlib only,
  no external dependencies).
- `python3 -m py_compile` passes on all modules.

## Known gaps

- No per-shift edit/update command.
- Default storage file path is `~/.gigtrack/shifts.json` (overridable via
  `--storage` or `GIGTRACK_STORAGE`).
- No git identity configuration in repo; commits use the existing local git
  identity.
- No `.github/workflows` files (intentionally omitted per requirements).
- No secrets, API keys, or personal data in any file.

## Credit

Built by Dylan Asdale for Asdale Dynamics, LLC (Indiana, formed October 2026).
MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.
