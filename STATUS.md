# STATUS

## What was built

A local-first Python CLI for small businesses to log expenses by category,
track totals, and export CSV or PDF summaries. Built for Asdale Dynamics, LLC.

No cloud, no accounts, no tracking — all data lives in a single JSON file on
your machine.

Files:
- `expense_tracker.py` — the CLI (argparse). Commands: `add`, `list`,
  `summary`, `export --format csv|pdf --output <file>`. Global `--storage`
  selects the local JSON file (default `expenses.json`). `--dry-run` on `add`
  and `export` previews changes without saving or writing anything. `--version`
  shows the version.
- `tests/test_expense_tracker.py` — 22 tests covering totals by category,
  grand totals, date parsing/validation, amount parsing/validation,
  case-sensitive categories, special characters, dry-run non-persistence,
  list output, save/load roundtrip, and CSV/PDF export.
- `LICENSE` — MIT License, copyright line exactly
  `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `README.md` — beginner-friendly usage instructions and credit to Asdale
  Dynamics, LLC.
- `.gitignore` — keeps runtime data (`expenses.json`, `__pycache__`, etc.) out
  of git.
- `STATUS.md` — this file.

## How to run it

```bash
# Install the PDF dependency
pip install reportlab

# Add expenses (stored locally in expenses.json)
python expense_tracker.py add --amount 12.50 --category Office --date 2026-10-28 --description "Pens"
python expense_tracker.py add --amount 45.00 --category Software --date 2026-10-28 --description "Subscription"

# Track totals
python expense_tracker.py summary
python expense_tracker.py list

# Export summaries
python expense_tracker.py export --format csv --output expenses.csv
python expense_tracker.py export --format pdf --output summary.pdf

# Dry-run (preview only, nothing saved)
python expense_tracker.py add --amount 10.00 --category Travel --date 2026-10-29 --description "Train" --dry-run
python expense_tracker.py export --format pdf --output summary.pdf --dry-run

# Check version
python expense_tracker.py --version

# Run tests
pytest
```

## Verification results

- `pytest`: 22 passed (0 failures)
- `ruff check`: all checks passed
- `ruff format --check`: both files already formatted
- Manual smoke test: `add`, `list`, `summary`, CSV export, PDF export,
  `--dry-run`, `--version`, invalid dates/amounts all work as expected;
  dry-run writes nothing to disk.
- LICENSE copyright line verified: `Copyright (c) 2026 Asdale Dynamics, LLC`
- README credits Asdale Dynamics, LLC at dylanasdale.github.io

## Known gaps

- PDF export is a simple single-page summary (totals by category + grand
  total), not an itemized statement.
- Storage is a single local JSON file; no encryption, no sync, no multiple
  workspaces beyond the `--storage` path.
- No GUI or web interface; CLI only.
- Amounts are stored as floats rounded to 2 decimals; for high-volume
  bookkeeping, a Decimal-based store could be considered.
- No edit/delete command for existing expenses yet.
- No `--since`/`--until` date filtering on `list`/`summary`/`export` yet.
