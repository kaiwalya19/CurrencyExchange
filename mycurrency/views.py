
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Currency, CurrencyExchangeRate
from django.conf import settings
import datetime
from .serializers import CurrencySerializer
from .adapters import CurrencyBeaconProvider
from decimal import Decimal

# Currency List & Create View
class CurrencyListCreateView(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

# Currency Detail View
class CurrencyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

# Retrieve Exchange Rates
class CurrencyRateListView(APIView):
    def get(self, request):
        source_currency = request.query_params.get('source_currency')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        rates = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency,
            valuation_date__range=[date_from, date_to]
        ).values('source_currency__code', 'exchanged_currency__code', 'valuation_date', 'rate_value')

        return Response(list(rates))
    
# Convert Currency
class CurrencyConvertView(APIView):
    def get(self, request):
        source_currency = request.query_params.get('source_currency')
        target_currency = request.query_params.get('target_currency')
        amount = Decimal(request.query_params.get('amount', 1))  # Convert amount to Decimal

        # Check if the rate exists in the database
        rate = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency,
            exchanged_currency__code=target_currency
        ).order_by('-valuation_date').first()

        if rate:
            # Use the rate from the database
            converted_amount = amount * rate.rate_value
            return Response({
                'rate': rate.rate_value,
                'converted_amount': converted_amount
            })
        else:
            # Fallback to external provider
            provider = CurrencyBeaconProvider()
            external_rate = provider.get_exchange_rate_data(
                source_currency, target_currency
            )
            if external_rate:
                # Use the external rate and optionally save it in the database
                rate_value = Decimal(external_rate['rate_value'])  # Ensure rate is Decimal
                CurrencyExchangeRate.objects.create(
                    source_currency=Currency.objects.get(code=source_currency),
                    exchanged_currency=Currency.objects.get(code=target_currency),
                    valuation_date=datetime.date.today(),
                    rate_value=rate_value
                )
                converted_amount = amount * rate_value
                return Response({
                    'rate': rate_value,
                    'converted_amount': converted_amount
                })
            else:
                # Return an error if no rate is found
                return Response({'error': 'Exchange rate not found'}, status=404)