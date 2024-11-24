from celery import shared_task
from .adapters import CurrencyBeaconProvider
from .models import Currency, CurrencyExchangeRate
import datetime

@shared_task
def fetch_historical_rates(source_currency, target_currency, start_date, end_date):
    provider = CurrencyBeaconProvider()
    current_date = start_date
    while current_date <= end_date:
        rate_data = provider.get_exchange_rate_data(
            source_currency, target_currency, valuation_date=current_date
        )
        if rate_data:
            CurrencyExchangeRate.objects.create(
                source_currency=Currency.objects.get(code=source_currency),
                exchanged_currency=Currency.objects.get(code=target_currency),
                valuation_date=current_date,
                rate_value=rate_data['rate_value']
            )
        current_date += datetime.timedelta(days=1)
        


@shared_task
def test_task():
    return "Task executed successfully!"

