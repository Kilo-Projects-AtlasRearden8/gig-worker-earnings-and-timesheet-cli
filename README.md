# gigtrack

A local-first CLI for logging gig and on-call work hours, earnings, expenses, and shift types. Built for nurses, gig workers, and anyone juggling multiple paychecks. Stores everything in a local JSON file and exports to CSV. No accounts, no keys, no cloud — your data stays on your machine.

Created by **Dylan Asdale** and published by **Asdale Dynamics, LLC** (Indiana, formed October 2026) — beginner-friendly AI education, books, and practical tools. Credit: Asdale Dynamics, LLC.

## What it does

- `add` — log a shift: date, employer/gig name, shift type (gig, on-call, per-diem, contract…), hours, rate, earnings, expenses
- `list` — view every shift with a running grand total
- `summary` — weekly totals (hours, earnings, expenses, net) grouped by ISO week
- `jobs` — per-job tallies with average hourly rate
- `export` — dump all shifts to CSV
- `delete` — remove a shift by id

## Install

```bash
git clone https://github.com/Asdale-Dynamics/gig-worker-earnings-and-timesheet-cli
cd gig-worker-earnings-and-timesheet-cli
pip install -e .
```

Or run without installing:

```bash
python -m gigtrack add --date 2026-10-30 --job "Hospital A" --type on-call --hours 12 --rate 45 --expenses 15.50
```

## Usage examples

Log a shift (earnings default to hours × rate when omitted):

```bash
gigtrack add --date 2026-10-30 --job "Hospital A" --type on-call --hours 12 --rate 45 --expenses 15.50
```

List all shifts:

```bash
gigtrack list
```

Weekly summary:

```bash
gigtrack summary
```

Per-job tallies:

```bash
gigtrack jobs
```

Export to CSV:

```bash
gigtrack export --out shifts.csv
```

Delete a shift (use the first 8 characters of its id):

```bash
gigtrack delete --id a1b2c3d4
```

Use a different storage file:

```bash
gigtrack --storage /path/to/my-shifts.json list
```

Data is stored locally in JSON (default: `~/.gigtrack/shifts.json`). Nothing is sent anywhere.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests cover the math (earnings, net, weekly totals, per-job tallies) and the date logic (ISO week parsing, week boundaries, year rollover).

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## About

Asdale Dynamics, LLC is a beginner-friendly AI education and small-tools studio founded by Dylan Asdale, registered nurse turned AI author of *The Massive AI Manual* (dylanasdale.github.io). This tool is part of the LLC's open-source apps and templates line: practical, local-first software anyone can use and sell.
