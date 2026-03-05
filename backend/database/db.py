# backend/database/db.py

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import func
from sqlalchemy import DateTime
from sqlalchemy import Boolean

from datetime import date


engine = create_engine("sqlite:///bnr.db", echo = False)
metadata = MetaData()

exchange_rates = Table (
    "exchange_rates",
    metadata,
    Column ("id", Integer, primary_key = True),
    Column ("currency", String, nullable = False),
    Column ("value", Float, nullable = False),
    Column ("date", Date, nullable = False),
)

alert_settings = Table(
    "alert_settings",
    metadata,
    Column("id", Integer, primary_key = True),
    Column("user_email", String, nullable = False),
    Column("currency", String, nullable = False),
    Column("threshold_percent", Float, nullable = False),
    Column("is_active", Boolean, default = True),
    Column("created_at", DateTime, default = func.now())
)

alert_logs = Table(
    "alert_logs",
    metadata,
    Column("id", Integer, primary_key = True),
    Column("currency", String, nullable = False),
    Column("old_value", Float, nullable = False),
    Column("new_value", Float, nullable = False),
    Column("change_percent", Float, nullable = False),
    Column("user_email", String, nullable = False),
    Column("rate_date", Date, nullable=False),
    Column("sent_at", DateTime, default = func.now())
)

metadata.create_all(engine)
