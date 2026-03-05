# backend/etl/load.py

import logging
from datetime import datetime
from sqlalchemy import insert, select

from database.db import engine, exchange_rates

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseLoader:

    @staticmethod
    def check_data_exists(date_str: str) -> bool:

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        with engine.connect() as conn:
            stmt = select(exchange_rates).where(exchange_rates.c.date == date_obj)
            result = conn.execute(stmt).fetchone()

        return result is not None
    
    @staticmethod
    def save_rates(date_str: str, rates):

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        if DatabaseLoader.check_data_exists(date_str):
            raise ValueError(f"Data for {date_str} already exists")
        
        with engine.begin() as conn:
            for rate in rates:
                stmt = insert(exchange_rates).values(
                    currency = rate['currency'],
                    value = rate['value'],
                    date = date_obj
                )
                conn.execute(stmt)
        
        logger.info(f"Loaded {len(rates)} records in the database")
        return len(rates)
    
def load(date_str: str, rates):

    loader = DatabaseLoader()
    return loader.save_rates(date_str, rates)