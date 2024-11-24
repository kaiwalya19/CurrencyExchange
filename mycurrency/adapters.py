import requests
from django.conf import settings



class CurrencyBeaconProvider:
    def get_exchange_rate_data(self, source_currency, target_currency, valuation_date=None):
        # Base URL for CurrencyBeacon API
        url = "https://api.currencybeacon.com/v1/latest"
        params = {
            'api_key': settings.CURRENCYBEACON_API_KEY,
            'base': source_currency,
            'symbols': target_currency
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            rate = data.get('rates', {}).get(target_currency)
            if rate:
                return {
                    'rate_value': rate
                }
        return None


class MockProvider:
    import random
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        return {
            "source_currency": source_currency,
            "exchanged_currency": exchanged_currency,
            "valuation_date": valuation_date,
            "rate_value": round(random.uniform(0.5, 1.5), 6)
        }
    