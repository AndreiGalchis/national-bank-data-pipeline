# baxkend/services/bnr_service.py

import requests
import xmltodict

from database.read_rates import get_rate_for_conversion

def convert_currency(from_currency: str, to_currency: str, amount: float):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency == "RON":
        to_rate = get_rate_for_conversion(to_currency)
        if to_rate > 1:
            converted_amount = amount / to_rate
        else:
            converted_amount = amount * to_rate

    if to_currency == "RON":
        from_rate = get_rate_for_conversion(from_currency)
        if from_rate > 1:
            converted_amount = amount * from_rate
        else:
            converted_amount = amount / to_rate
        
    if from_currency != "RON" and to_currency != "RON":
        from_rate = get_rate_for_conversion(from_currency)
        to_rate = get_rate_for_conversion(to_currency)
        
        converted_amount = amount * (from_rate / to_rate)

    return round(converted_amount, 4)
