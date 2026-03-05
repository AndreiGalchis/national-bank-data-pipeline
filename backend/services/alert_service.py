import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
from datetime import datetime

from database.read_rates import get_previous_rate_and_date, get_today_rate
from database.alerts_db import get_active_alerts, log_sent_alert, was_alert_sent_for_date

logging.basicConfig(level=logging.INFO)

def calculate_percentage_change(old_rate: float, new_rate: float):
    return ((new_rate - old_rate) / old_rate) * 100

def check_and_trigger_alerts(current_date_str):
    date_obj = datetime.strptime(current_date_str, "%Y-%m-%d").date()
    alerts_to_send = []
    active_alerts = get_active_alerts()

    for alert_config in active_alerts:
        currency_name = alert_config['currency']
        threshold = alert_config['threshold_percent']
        user_email = alert_config['user_email']

        if was_alert_sent_for_date(currency_name, user_email, date_obj):
            continue

        previous_data = get_previous_rate_and_date(currency_name, date_obj)
        if not previous_data:
            continue
            
        old_rate = previous_data.value
        new_rate = get_today_rate(currency_name, date_obj)
        if not new_rate:
            continue

        change = calculate_percentage_change(old_rate, new_rate)

        if abs(change) >= threshold:
            direction = "increased" if change > 0 else "decreased"
            alert_data = {
                "currency": currency_name,
                "old_rate": old_rate,
                "new_rate": new_rate,
                "change_percent": change,
                "user_email": user_email,
                "message": f"{currency_name}/RON has {direction} by {abs(change):.2f}% today (from {old_rate:.4f} to {new_rate:.4f})"
            }
            alerts_to_send.append(alert_data)
            
            # Trimitem și data_obj (data BNR) către log
            log_sent_alert(currency_name, old_rate, new_rate, change, user_email, date_obj)

    return alerts_to_send

def send_alert_email(alert_data: dict):
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        logging.error("SENDER_EMAIL or SENDER_PASSWORD not set in .env file")
        return False
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = alert_data['user_email']
    msg['Subject'] = f"BNR Alert: {alert_data['currency']} changed"

    body = f"""
    Hello,

    {alert_data['message']}

    Details:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Currency:       {alert_data['currency']}/RON
    Previous rate:  {alert_data['old_rate']:.4f} RON
    Current rate:   {alert_data['new_rate']:.4f} RON
    Change:         {alert_data['change_percent']:+.2f}%
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    This is an automated alert from your BNR Rate Monitor.
    """
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        logging.info(f"✅ Email sent successfully to {alert_data['user_email']}")
        return True
    except Exception as e:
        logging.error(f"Email error: {e}")
        return False
