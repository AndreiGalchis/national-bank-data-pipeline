#main

from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI
from fastapi import HTTPException

from etl.pipeline import run_etl_pipeline

from services.bnr_service import convert_currency
from services.alert_service import check_and_trigger_alerts
from services.alert_service import send_alert_email

from database.read_rates import get_latest_rates
from database.alerts_db import create_alert
from database.alerts_db import get_user_alerts
from database.alerts_db import delete_alert

import logging


app = FastAPI()

@app.post("/api/update/exchange-rates")
def update_rates_and_check_alerts():

    try:
        etl_result = run_etl_pipeline(source = "bnr")

        if etl_result["status"] != "success":
            raise HTTPException(status_code = 500, detail = f"ETL failed: {etl_result.get('error')}")


        bnr_date = etl_result["date"]

        #check and trigger alerts
        alerts_triggered = check_and_trigger_alerts(bnr_date)

        emails_sent = 0
        for alert in alerts_triggered:
            if send_alert_email(alert): 
                emails_sent += 1

        return {
            "status": "success",
            "date": bnr_date,
            "rates_count": etl_result["records_loaded"],
            "alerts_triggered": len(alerts_triggered),
            "emails_sent": emails_sent,
            "etl_duration_in_seconds": etl_result["duration_seconds"]
        }
    
    except ValueError as e:
        raise HTTPException(status_code=409, detail=f"Data already exists: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")



@app.get("/api/rates/latest")
def read_latest_rates_from_db():
    return get_latest_rates()

@app.get("/api/convert")
def convert(from_currency: str, to_currency: str, amount: float):
    try:
        result = convert_currency(from_currency, to_currency, amount)
        return {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "amount": amount,
            "converted": result
        }
    except ValueError as err:
        raise HTTPException(status_code = 400, detail = str(err))
    
@app.post("/api/create-alerts")
def create_new_alert(user_email: str, currency_name: str, threshold_percent: float):
    if threshold_percent <= 0:
        raise HTTPException(status_code = 400, detail = "Threshold must be positive")
    
    create_alert(user_email, currency_name, threshold_percent)

    return {
        "message": f"Alert created: You will be notified when {currency_name.upper()} changes by ± {threshold_percent}%"
    }

@app.get("/api/get-user-alerts")
def get_alerts_by_user(user_email: str):
    alerts = get_user_alerts(user_email)
    return {
        "user_email": user_email,
        "alerts": alerts
    }

@app.delete("/api/delete-alert")
def remove_alert(alert_id: int):
    delete_alert(alert_id)
    return {"message": f"Alert with id = {alert_id} deleted"}

