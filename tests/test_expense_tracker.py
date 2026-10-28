"""Tests for the business expense tracker CLI.

Covers totals by category, grand totals, date parsing/validation, amounts,
and dry-run behavior (nothing is persisted).
"""

from __future__ import annotations

import os
from datetime import date

import pytest

from expense_tracker import (
    ExpenseTrackerError,
    add_expense,
    export_csv,
    export_pdf,
    grand_total,
    load_expenses,
    parse_amount,
    parse_date,
    totals_by_category,
)


def sample_expenses() -> list[dict]:
    return [
        {
            "amount": 12.50,
            "category": "Office",
            "date": "2026-10-01",
            "description": "Pens",
        },
        {
            "amount": 45.00,
            "category": "Software",
            "date": "2026-10-02",
            "description": "Editor subscription",
        },
        {
            "amount": 8.75,
            "category": "Office",
            "date": "2026-10-03",
            "description": "Sticky notes",
        },
    ]


def test_totals_by_category():
    expenses = sample_expenses()
    totals = totals_by_category(expenses)
    assert totals == {"Office": 21.25, "Software": 45.00}


def test_grand_total():
    expenses = sample_expenses()
    assert grand_total(expenses) == 66.25


def test_grand_total_empty():
    assert grand_total([]) == 0.0


def test_parse_date_valid():
    assert parse_date("2026-10-28") == date(2026, 10, 28)
    assert parse_date("2026-01-01") == date(2026, 1, 1)


def test_parse_date_invalid():
    for bad in ["10-28-2026", "2026-13-01", "not-a-date", "", "2026/10/28"]:
        with pytest.raises(ExpenseTrackerError):
            parse_date(bad)


def test_parse_amount_valid():
    assert parse_amount("12.50") == 12.50
    assert parse_amount("100") == 100.0
    assert parse_amount("0.01") == 0.01


def test_parse_amount_invalid():
    for bad in ["abc", "-5.00", "0", "0.00", ""]:
        with pytest.raises(ExpenseTrackerError):
            parse_amount(bad)


def test_add_expense_persists_locally(tmp_path):
    storage = os.path.join(tmp_path, "expenses.json")
    expenses: list[dict] = []
    entry = add_expense(
        expenses,
        20.00,
        "Travel",
        date(2026, 10, 5),
        "Train ticket",
        storage,
        dry_run=False,
    )
    assert entry["amount"] == 20.00
    assert entry["category"] == "Travel"
    assert entry["date"] == "2026-10-05"
    assert entry["description"] == "Train ticket"
    assert os.path.exists(storage)
    saved = load_expenses(storage)
    assert len(saved) == 1
    assert saved[0]["amount"] == 20.00


def test_add_expense_dry_run_does_not_persist(tmp_path):
    storage = os.path.join(tmp_path, "expenses.json")
    expenses: list[dict] = []
    add_expense(
        expenses,
        20.00,
        "Travel",
        date(2026, 10, 5),
        "Train ticket",
        storage,
        dry_run=True,
    )
    assert not os.path.exists(storage)
    assert expenses == []


def test_export_csv(tmp_path):
    expenses = sample_expenses()
    output = os.path.join(tmp_path, "out.csv")
    export_csv(expenses, output, dry_run=False)
    assert os.path.exists(output)
    with open(output, newline="", encoding="utf-8") as handle:
        lines = handle.read().strip().splitlines()
    assert lines[0] == "date,category,amount,description"
    assert len(lines) == 4  # header + 3 expenses


def test_export_csv_dry_run_does_not_write(tmp_path):
    expenses = sample_expenses()
    output = os.path.join(tmp_path, "out.csv")
    export_csv(expenses, output, dry_run=True)
    assert not os.path.exists(output)


def test_export_pdf(tmp_path):
    expenses = sample_expenses()
    output = os.path.join(tmp_path, "summary.pdf")
    export_pdf(expenses, output, dry_run=False)
    assert os.path.exists(output)
    assert os.path.getsize(output) > 0


def test_export_pdf_dry_run_does_not_write(tmp_path):
    expenses = sample_expenses()
    output = os.path.join(tmp_path, "summary.pdf")
    export_pdf(expenses, output, dry_run=True)
    assert not os.path.exists(output)
