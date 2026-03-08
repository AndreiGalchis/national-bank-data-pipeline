from datetime import datetime
import pytest
from sqlalchemy import delete

from etl.load import load
from database.db import engine, exchange_rates

def cleanup_date(date_str: str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    with engine.begin() as conn:
        stmt = delete(exchange_rates).where(exchange_rates.c.date == date_obj)
        conn.execute(stmt)


def test_load_inserts_records():
    date_str = "2099-01-01"
    rates = [
        {"currency": "USD", "value": 4.55, "date": date_str},
        {"currency": "EUR", "value": 4.98, "date": date_str},
    ]

    cleanup_date(date_str)

    inserted = load(date_str, rates)
    assert inserted == 2

    cleanup_date(date_str)

def test_load_block_duplicate():
    date_str = "2099-01-02"
    rates = [
        {"currency": "USD", "value": 4.55, "date": date_str},
        {"currency": "EUR", "value": 4.98, "date": date_str},
    ]

    cleanup_date(date_str)

    first_insert = load(date_str, rates)
    assert first_insert == 2

    with pytest.raises(ValueError, match = "already exists"):
        load(date_str, rates)

    cleanup_date(date_str)

