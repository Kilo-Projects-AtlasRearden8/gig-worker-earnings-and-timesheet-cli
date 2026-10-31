# gigtrack

A friendly, local-first command-line tool for logging gig and on-call work
hours, earnings, expenses, and shift types. Built for nurses, gig workers, and
anyone juggling multiple paychecks. Everything stays on your computer in a
simple JSON file — no accounts, no API keys, no cloud, nothing is ever sent
anywhere. Export your records to CSV whenever you need them.

Created by **Dylan Asdale** and published by **Asdale Dynamics, LLC**
(Indiana, formed October 2026) — beginner-friendly AI education, books, and
practical tools. Credit: Asdale Dynamics, LLC.

## What it does

| Command | What it does |
|---------|-------------|
| `add` | Log a shift: date, employer or gig name, shift type, hours, rate, earnings, expenses |
| `list` | See every shift you've recorded, with a grand total at the bottom |
| `summary` | Weekly totals (hours, earnings, expenses, net pay), grouped by week |
| `jobs` | Totals per employer/gig, with your average hourly rate for each |
| `export` | Save all your shifts to a CSV file (opens in Excel, Google Sheets, etc.) |
| `delete` | Remove a shift by its ID |

Shift types are whatever makes sense for your work — gig, on-call, per-diem,
contract, registry, and so on.

## Install

You need Python 3.8 or newer. No extra packages to install — gigtrack uses
only what comes with Python.

**Option 1: Run from the folder (no installation)**

```bash
cd /path/to/gig-worker-earnings-and-timesheet-cli
python3 -m gigtrack add --date 2026-10-30 --job "Hospital A" \
  --type on-call --hours 12 --rate 45 --expenses 15.50
```

**Option 2: Install it (recommended if you'll use it regularly)**

```bash
cd /path/to/gig-worker-earnings-and-timesheet-cli
pip install -e .
```

After installing, just type `gigtrack` instead of `python3 -m gigtrack`.

## Where your data lives

By default, shifts are saved to `~/.gigtrack/shifts.json` on your computer.
You can point gigtrack at a different file with `--storage`, or set the
`GIGTRACK_STORAGE` environment variable:

```bash
# One-off different file
gigtrack --storage /path/to/my-shifts.json list

# Or set it once for your session
export GIGTRACK_STORAGE="/path/to/my-shifts.json"
gigtrack list
```

Nothing is stored online. Your data never leaves your machine.

## Step-by-step examples

### Log your first shift

```bash
python3 -m gigtrack add \
  --date 2026-10-30 \
  --job "Hospital A" \
  --type on-call \
  --hours 12 \
  --rate 45 \
  --expenses 15.50
```

Earnings are worked out for you (hours × rate) if you leave out `--earnings`.

### See everything you've logged

```bash
python3 -m gigtrack list
```

You'll get a line per shift plus a grand total at the bottom.

### Check this week's earnings

```bash
python3 -m gigtrack summary
```

Prints a breakdown by ISO week (Monday–Sunday), plus all-time totals.

### See how much each job has paid you

```bash
python3 -m gigtrack jobs
```

Shows hours, earnings, expenses, net pay, and your average hourly rate per
employer or gig.

### Export to a spreadsheet

```bash
python3 -m gigtrack export --out my-shifts.csv
```

Open `my-shifts.csv` in Excel, Google Sheets, Numbers, or any spreadsheet app.

### Remove a shift

Each shift gets an ID when you create it (shown when you add it and when you
list shifts). You can delete with the full ID or just the first several
characters, as long as that's enough to tell it apart from your other shifts:

```bash
python3 -m gigtrack delete --id a1b2c3d4
```

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

Tests cover the money math (earnings, net pay, totals, per-job tallies) and
the date logic (ISO week grouping, week boundaries, year rollover).

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## About

Asdale Dynamics, LLC is a beginner-friendly AI education and small-tools studio
founded by Dylan Asdale, a registered nurse turned AI author of
*The Massive AI Manual* (dylanasdale.github.io). This tool is part of the
LLC's open-source apps and templates line: practical, local-first software
anyone can use, share, and sell.
