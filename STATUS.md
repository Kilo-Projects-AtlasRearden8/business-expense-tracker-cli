# STATUS

## What was built

A local-first Python CLI for small businesses to log expenses by category,
track totals, and export CSV or PDF summaries. Built for Asdale Dynamics, LLC.

Files:
- `expense_tracker.py` — the CLI (argparse). Commands: `add`, `list`, `summary`,
  `export --format csv|pdf --output <file>`. Global `--storage` selects the
  local JSON file (default `expenses.json`). `--dry-run` on `add` and `export`
  previews changes without saving or writing anything.
- `tests/test_expense_tracker.py` — 13 tests covering totals by category, grand
  totals, date parsing/validation, amount validation, CSV/PDF export, and
  dry-run non-persistence.
- `LICENSE` — MIT License, copyright line exactly
  `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `README.md` — usage instructions and credit to Asdale Dynamics, LLC.
- `.gitignore` — keeps runtime data (`expenses.json`, `__pycache__`, etc.) out of git.

No cloud, no accounts, no API keys, no secrets, no personal data. No
`.github/workflows` files.

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

# Run tests
pytest
```

## Verification results

- `pytest`: 13 passed
- `ruff check`: all checks passed
- `ruff format --check`: both files already formatted
- Manual smoke test: `add`, `list`, `summary`, CSV export, PDF export, and
  `--dry-run` all work; invalid dates/amounts are rejected; dry-run writes
  nothing to disk.

## Known gaps

- PDF export is a simple single-page summary (totals by category + grand
  total), not an itemized statement.
- Storage is a single local JSON file; no encryption, no sync, no multiple
  workspaces beyond the `--storage` path.
- No GUI or web interface; CLI only.
- Amounts are stored as floats rounded to 2 decimals; for high-volume
  bookkeeping, a Decimal-based store could be considered.
