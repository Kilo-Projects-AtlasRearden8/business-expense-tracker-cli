# Business Expense Tracker CLI

A small, local-first Python command-line tool for logging business expenses by
category, tracking totals, and exporting CSV or PDF summaries. Built for small
business owners, freelancers, and authors who want simple bookkeeping without
the cloud.

Created by **Asdale Dynamics, LLC** (Indiana) — beginner-friendly AI education,
books and guides, and practical tools. Learn more at dylanasdale.github.io.

## Features

- **Log expenses** with amount, category, date, and optional description
- **Track totals** by category plus a grand total
- **Export** summaries to CSV or PDF
- **Dry-run mode** — preview changes without saving anything
- **Local-only storage** — everything lives in a single JSON file on your
  machine. No cloud, no accounts, no API keys, no personal data collected.

## Requirements

- Python 3.10+
- [reportlab](https://pypi.org/project/reportlab/) (for PDF export)

Install the dependency:

```bash
pip install reportlab
```

## Usage

Run from the project folder:

```bash
python expense_tracker.py add --amount 12.50 --category Office --date 2026-10-28 --description "Pens"
python expense_tracker.py add --amount 45.00 --category Software --date 2026-10-28 --description "Editor subscription"
python expense_tracker.py summary
python expense_tracker.py list
python expense_tracker.py export --format csv --output expenses.csv
python expense_tracker.py export --format pdf --output summary.pdf
```

Preview a change without saving it (dry-run):

```bash
python expense_tracker.py add --amount 10.00 --category Travel --date 2026-10-29 --description "Train" --dry-run
python expense_tracker.py export --format pdf --output summary.pdf --dry-run
```

Use a different local storage file:

```bash
python expense_tracker.py --storage my_expenses.json add --amount 5.00 --category Meals --date 2026-10-28 --description "Lunch"
```

## Running tests

```bash
pytest
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See [LICENSE](LICENSE).

## About Asdale Dynamics, LLC

Asdale Dynamics, LLC is an Indiana company founded by Dylan Asdale, a
registered nurse turned AI author and founder. The LLC publishes beginner
manuals on AI tools, agents, local AI, free AI coding, GitHub, automation, and
privacy, plus open-source tools like this one. More at
[dylanasdale.github.io](https://dylanasdale.github.io).
