# # backend/database/alerts_db.py

from sqlalchemy import select, insert, delete
from database.db import engine, alert_settings, alert_logs
from datetime import datetime, date

def create_alert(user_email: str, currency_name: str, threshold_percent: float):
    with engine.begin() as conn:
        stmt = insert(alert_settings).values(
            user_email=user_email,
            currency=currency_name.upper(),
            threshold_percent=threshold_percent
        )
        conn.execute(stmt)

def get_active_alerts():
    with engine.connect() as conn:
        stmt = select(alert_settings).where(alert_settings.c.is_active == True)
        result = conn.execute(stmt)
        return [dict(row._mapping) for row in result]

def get_user_alerts(user_email: str):
    with engine.connect() as conn:
        stmt = select(alert_settings).where(alert_settings.c.user_email == user_email)
        result = conn.execute(stmt)
        return [dict(row._mapping) for row in result]

def delete_alert(alert_id: int):
    with engine.begin() as conn:
        stmt = delete(alert_settings).where(alert_settings.c.id == alert_id)
        conn.execute(stmt)

def log_sent_alert(currency_name: str, old_rate: float, new_rate: float, change_percent: float, user_email: str, bnr_date: date):
    # Salvăm log ul cu tot cu DATA BNR (rate_date)
    with engine.begin() as conn:
        stmt = insert(alert_logs).values(
            user_email=user_email,
            currency=currency_name,
            old_value=old_rate,
            new_value=new_rate,
            change_percent=change_percent,
            rate_date=bnr_date,  # data cursului
            sent_at=datetime.now()
        )
        conn.execute(stmt)

def was_alert_sent_for_date(currency_name: str, user_email: str, bnr_date: date):

    # verifica daca exista deja un log pt data asta de curs (rate_date)

    with engine.connect() as conn:
        stmt = select(alert_logs).where(
            alert_logs.c.currency == currency_name,
            alert_logs.c.user_email == user_email,
            alert_logs.c.rate_date == bnr_date 
        )
        result = conn.execute(stmt).fetchone()
        return True if result else False