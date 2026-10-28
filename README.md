# Business Expense Tracker CLI

A friendly, local-first command-line tool for logging business expenses by
category, tracking totals, and exporting clean CSV or PDF summaries.

Built for small business owners, freelancers, and authors who want simple
bookkeeping without the cloud, without accounts, and without hassle.

---

## Why this tool?

- **No cloud, no accounts, no tracking** — your data stays in one JSON file on
  your machine
- **Beginner-friendly** — plain English errors, clear prompts, no jargon
- **Dry-run mode** — preview any change before it saves
- **Exports you can actually use** — CSV for spreadsheets, PDF for records
- **MIT licensed** — free to use, modify, and share

Created by **Asdale Dynamics, LLC** (Indiana) — beginner-friendly AI education,
books, guides, and practical tools. Learn more at
[dylanasdale.github.io](https://dylanasdale.github.io).

---

## Quick start

### 1. Install the PDF dependency

```bash
pip install reportlab
```

(CSV export works without any extra packages.)

### 2. Add your first expense

```bash
python expense_tracker.py add \
  --amount 12.50 \
  --category Office \
  --date 2026-10-28 \
  --description "Pens and notebooks"
```

You'll see:
```
Added Office expense of $12.50 on 2026-10-28.
```

### 3. Add a few more

```bash
python expense_tracker.py add --amount 45.00 --category Software --date 2026-10-28 --description "Editor subscription"
python expense_tracker.py add --amount 8.75 --category Office --date 2026-10-29 --description "Sticky notes"
```

### 4. See your totals

```bash
python expense_tracker.py summary
```

Output:
```
CATEGORY                TOTAL
------------------------------
Office           $      21.25
Software         $      45.00
------------------------------
TOTAL            $      66.25
```

### 5. List everything

```bash
python expense_tracker.py list
```

### 6. Export for your records

**CSV (opens in Excel, Google Sheets, etc.):**
```bash
python expense_tracker.py export --format csv --output expenses.csv
```

**PDF (clean summary for filing):**
```bash
python expense_tracker.py export --format pdf --output summary.pdf
```

---

## Dry-run mode — preview before you commit

Not sure about an entry? Want to see what a PDF would look like without
creating a file? Use `--dry-run`:

```bash
# Preview adding an expense
python expense_tracker.py add --amount 10.00 --category Travel --date 2026-10-29 --description "Train" --dry-run

# Preview a PDF export
python expense_tracker.py export --format pdf --output summary.pdf --dry-run
```

Nothing is saved or written. You'll see exactly what *would* happen.

---

## Using a different storage file

By default, expenses live in `expenses.json` in the current folder. Use
`--storage` to keep separate books (e.g., one per business, per year, per
project):

```bash
python expense_tracker.py --storage 2026_business.json add --amount 5.00 --category Meals --date 2026-10-28 --description "Lunch"
python expense_tracker.py --storage 2026_business.json summary
```

---

## Full command reference

```
python expense_tracker.py [--storage FILE] <command> [options]

Commands:
  add       Add a new expense
  list      List all recorded expenses
  summary   Show totals by category and grand total
  export    Export expenses to CSV or PDF

Options:
  --storage FILE   Local JSON storage file (default: expenses.json)
  --version        Show version and exit
  -h, --help       Show help
```

### `add` — log a new expense

```
python expense_tracker.py add --amount AMOUNT --category CATEGORY --date DATE [--description TEXT] [--dry-run]
```

| Option          | Required? | Description                              |
|-----------------|-----------|------------------------------------------|
| `--amount`      | Yes       | Positive number (e.g., `12.50`)          |
| `--category`    | Yes       | Category name (e.g., `Office`, `Travel`) |
| `--date`        | Yes       | Date in `YYYY-MM-DD` format              |
| `--description` | No        | Free-text note                           |
| `--dry-run`     | No        | Preview only, don't save                 |

### `list` — show all expenses

```
python expense_tracker.py list
```

### `summary` — show totals

```
python expense_tracker.py summary
```

### `export` — save a report

```
python expense_tracker.py export --format csv|pdf --output FILE [--dry-run]
```

| Option     | Required? | Description                          |
|------------|-----------|--------------------------------------|
| `--format` | Yes       | `csv` or `pdf`                       |
| `--output` | Yes       | Output file path                     |
| `--dry-run`| No        | Preview only, don't write file       |

---

## Running the tests

```bash
pytest
```

You should see 13 tests pass, covering:
- Category totals and grand totals
- Date parsing and validation
- Amount parsing and validation
- Dry-run behavior (nothing saved)
- CSV and PDF export

---

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.
See [LICENSE](LICENSE) for full text.

---

## About Asdale Dynamics, LLC

Asdale Dynamics, LLC is an Indiana company founded by Dylan Asdale, a
registered nurse turned AI author and founder. The LLC publishes beginner
manuals on AI tools, agents, local AI, free AI coding, GitHub, automation, and
privacy — plus open-source tools like this one.

More at [dylanasdale.github.io](https://dylanasdale.github.io).