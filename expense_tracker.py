"""Business expense tracker CLI.

Log expenses by category, track totals, and export CSV or PDF summaries.
Stores everything locally (a single JSON file). No cloud, no accounts, no
secrets.

Usage:
    python expense_tracker.py add --amount 12.50 --category Office --date 2026-10-28 --description "Pens"
    python expense_tracker.py summary
    python expense_tracker.py export --format csv --output expenses.csv
    python expense_tracker.py export --format pdf --output summary.pdf --dry-run
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import date, datetime
from typing import Any

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DEFAULT_STORAGE = "expenses.json"
DATE_FORMAT = "%Y-%m-%d"
VERSION = "1.0.0"


class ExpenseTrackerError(Exception):
    """Raised for user-facing input or storage errors."""


def parse_date(value: str) -> date:
    """Parse a YYYY-MM-DD string into a date, or raise ExpenseTrackerError."""
    try:
        return datetime.strptime(value, DATE_FORMAT).date()
    except (ValueError, TypeError):
        raise ExpenseTrackerError(
            f"Invalid date '{value}'. Use YYYY-MM-DD (e.g. 2026-10-28)."
        )


def parse_amount(value: str) -> float:
    """Parse a positive monetary amount, or raise ExpenseTrackerError."""
    try:
        amount = float(value)
    except (ValueError, TypeError):
        raise ExpenseTrackerError(f"Invalid amount '{value}'. Must be a number.")
    if amount <= 0:
        raise ExpenseTrackerError("Amount must be greater than zero.")
    return round(amount, 2)


def load_expenses(path: str) -> list[dict[str, Any]]:
    """Load expenses from the local JSON storage file."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ExpenseTrackerError(f"Storage file '{path}' is corrupted: {exc}") from exc
    if not isinstance(data, list):
        raise ExpenseTrackerError(f"Storage file '{path}' must contain a list.")
    return data


def save_expenses(path: str, expenses: list[dict[str, Any]]) -> None:
    """Persist expenses to the local JSON storage file."""
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        json.dump(expenses, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    os.replace(tmp_path, path)


def add_expense(
    expenses: list[dict[str, Any]],
    amount: float,
    category: str,
    expense_date: date,
    description: str,
    storage_path: str,
    dry_run: bool,
) -> dict[str, Any]:
    """Add one expense. Unless dry_run, writes to local storage."""
    entry: dict[str, Any] = {
        "amount": amount,
        "category": category.strip(),
        "date": expense_date.isoformat(),
        "description": description.strip(),
    }
    if dry_run:
        print("[dry-run] Would add expense:")
        print(
            f"  {entry['date']}  {entry['category']}  ${entry['amount']:.2f}  {entry['description']}"
        )
        print("[dry-run] Nothing saved.")
        return entry
    expenses.append(entry)
    save_expenses(storage_path, expenses)
    print(
        f"Added {entry['category']} expense of ${entry['amount']:.2f} on {entry['date']}."
    )
    return entry


def list_expenses(expenses: list[dict[str, Any]]) -> None:
    """Print all expenses in date order."""
    if not expenses:
        print("No expenses recorded yet.")
        return
    ordered = sorted(expenses, key=lambda e: e.get("date", ""))
    print(f"{'DATE':<12} {'CATEGORY':<16} {'AMOUNT':>10}  DESCRIPTION")
    print("-" * 60)
    for entry in ordered:
        print(
            f"{entry.get('date', ''):<12} "
            f"{entry.get('category', ''):<16} "
            f"{entry.get('amount', 0):>10.2f}  {entry.get('description', '')}"
        )


def totals_by_category(expenses: list[dict[str, Any]]) -> dict[str, float]:
    """Return a dict of category -> total amount."""
    totals: dict[str, float] = {}
    for entry in expenses:
        category = entry.get("category", "Uncategorized")
        totals[category] = round(
            totals.get(category, 0.0) + float(entry.get("amount", 0.0)), 2
        )
    return totals


def grand_total(expenses: list[dict[str, Any]]) -> float:
    """Return the sum of all expense amounts."""
    return round(sum(float(entry.get("amount", 0.0)) for entry in expenses), 2)


def summary(expenses: list[dict[str, Any]]) -> None:
    """Print totals by category and grand total."""
    totals = totals_by_category(expenses)
    if not totals:
        print("No expenses recorded yet.")
        return
    print(f"{'CATEGORY':<16} {'TOTAL':>12}")
    print("-" * 30)
    for category in sorted(totals):
        print(f"{category:<16} ${totals[category]:>11.2f}")
    print("-" * 30)
    print(f"{'TOTAL':<16} ${grand_total(expenses):>11.2f}")


def export_csv(expenses: list[dict[str, Any]], output: str, dry_run: bool) -> None:
    """Export expenses to CSV."""
    ordered = sorted(expenses, key=lambda e: e.get("date", ""))
    rows = [
        {
            "date": e.get("date", ""),
            "category": e.get("category", ""),
            "amount": f"{float(e.get('amount', 0.0)):.2f}",
            "description": e.get("description", ""),
        }
        for e in ordered
    ]
    if dry_run:
        print(f"[dry-run] Would export {len(rows)} expenses to CSV '{output}'.")
        for row in rows[:5]:
            print("  ", row)
        if len(rows) > 5:
            print(f"  ... and {len(rows) - 5} more row(s).")
        print("[dry-run] Nothing written.")
        return
    with open(output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["date", "category", "amount", "description"]
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Exported {len(rows)} expenses to CSV '{output}'.")


def export_pdf(expenses: list[dict[str, Any]], output: str, dry_run: bool) -> None:
    """Export a summary PDF with totals by category."""
    totals = totals_by_category(expenses)
    total = grand_total(expenses)

    def draw() -> None:
        c = canvas.Canvas(output, pagesize=letter)
        _width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, height - 72, "Business Expense Summary")
        c.setFont("Helvetica", 10)
        c.drawString(72, height - 92, f"Generated: {date.today().isoformat()}")
        c.drawString(
            72, height - 106, "Source: local expense tracker (no cloud storage)"
        )

        y = height - 140
        c.setFont("Helvetica-Bold", 12)
        c.drawString(72, y, "Totals by Category")
        y -= 24
        c.setFont("Helvetica", 11)
        if not totals:
            c.drawString(72, y, "No expenses recorded.")
        else:
            for category in sorted(totals):
                c.drawString(72, y, f"{category}: ${totals[category]:.2f}")
                y -= 20
        y -= 12
        c.setFont("Helvetica-Bold", 12)
        c.drawString(72, y, f"Grand Total: ${total:.2f}")
        c.showPage()
        c.save()

    if dry_run:
        print(
            f"[dry-run] Would export summary PDF to '{output}' ({len(expenses)} expense(s), ${total:.2f} total)."
        )
        print("[dry-run] Nothing written.")
        return
    draw()
    print(
        f"Exported summary PDF to '{output}' ({len(expenses)} expense(s), ${total:.2f} total)."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Log business expenses by category, track totals, and export CSV or PDF summaries.",
    )
    parser.add_argument(
        "--storage",
        default=DEFAULT_STORAGE,
        help=f"Local JSON storage file path (default: {DEFAULT_STORAGE})",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new expense.")
    add_parser.add_argument(
        "--amount", required=True, help="Expense amount (e.g. 12.50)."
    )
    add_parser.add_argument(
        "--category", required=True, help="Expense category (e.g. Office)."
    )
    add_parser.add_argument("--date", required=True, help="Expense date (YYYY-MM-DD).")
    add_parser.add_argument(
        "--description",
        default="",
        help="Optional description of the expense.",
    )
    add_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without saving anything.",
    )

    subparsers.add_parser("list", help="List all recorded expenses.")
    subparsers.add_parser("summary", help="Show totals by category and grand total.")

    export_parser = subparsers.add_parser(
        "export", help="Export expenses to CSV or PDF."
    )
    export_parser.add_argument(
        "--format",
        choices=["csv", "pdf"],
        required=True,
        help="Export format: csv or pdf.",
    )
    export_parser.add_argument("--output", required=True, help="Output file path.")
    export_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without writing any file.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        expenses = load_expenses(args.storage)

        if args.command == "add":
            expense_date = parse_date(args.date)
            amount = parse_amount(args.amount)
            add_expense(
                expenses,
                amount,
                args.category,
                expense_date,
                args.description,
                args.storage,
                args.dry_run,
            )
        elif args.command == "list":
            list_expenses(expenses)
        elif args.command == "summary":
            summary(expenses)
        elif args.command == "export":
            if args.format == "csv":
                export_csv(expenses, args.output, args.dry_run)
            else:
                export_pdf(expenses, args.output, args.dry_run)
        else:  # pragma: no cover - argparse guarantees a subcommand
            parser.error(f"Unknown command: {args.command}")
    except ExpenseTrackerError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
