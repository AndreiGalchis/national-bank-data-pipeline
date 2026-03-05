# backend/database/read_rates.py

from sqlalchemy import select
from sqlalchemy import func

from database.db import engine
from database.db import exchange_rates

from datetime import date


def get_latest_rates():
    with engine.connect() as conn:
        latest_date_query = conn.execute(select(func.max(exchange_rates.c.date)))
        latest_date = latest_date_query.scalar()

        if not latest_date:
            return []
        
        result = conn.execute(select(exchange_rates).where(exchange_rates.c.date == latest_date))

        return [
            {
                "currency": row.currency,
                "value": row.value,
                "date": row.date.isoformat()
            }
            for row in result
        ]
    
def get_rate_for_conversion(currency_name: str):
    with engine.connect() as conn:
        latest_date_query = conn.execute(select(func.max(exchange_rates.c.date)))
        latest_date = latest_date_query.scalar()

        if not latest_date:
            return None
        
        result = conn.execute(
                 select(exchange_rates.c.value)
                 .where(exchange_rates.c.currency == currency_name, exchange_rates.c.date == latest_date)).fetchone() 

        if result:
            return result.value
        else:
            return None

def get_previous_rate_and_date(currency_name: str, reference_date):   # gaseste cursul anterior si data anterioara (cu 1 zi lucratoare inainte) pt o moneda anume
    with engine.connect() as conn:
        stmt = select(exchange_rates.c.value, exchange_rates.c.date).where(
            exchange_rates.c.currency == currency_name,
            exchange_rates.c.date < reference_date
        ).order_by(exchange_rates.c.date.desc()).limit(1)
        result = conn.execute(stmt).fetchone()

        if result:
            return result
        return None
    
def get_today_rate(currency_name: str, today_date): # gaseste cursul pt o moneda data pt ziua de azi
    with engine.connect() as conn:
        stmt = select(exchange_rates.c.value).where(exchange_rates.c.currency == currency_name, exchange_rates.c.date == today_date)
        result = conn.execute(stmt).scalar()

        return result
