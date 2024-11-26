
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Currency, CurrencyExchangeRate
from django.conf import settings
import datetime
from .serializers import CurrencySerializer
from .adapters import CurrencyBeaconProvider
from decimal import Decimal
from django.core.cache import cache

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
        amount = float(request.query_params.get('amount', 0))

        cache_key = f"conversion-{source_currency}-{target_currency}-{amount}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result)

        rate = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency,
            exchanged_currency__code=target_currency
        ).order_by('-valuation_date').first()

        if not rate:
            return Response({"error": "Exchange rate not found."}, status=404)

        converted_amount = amount * float(rate.rate_value)
        result = {"converted_amount": converted_amount}
        cache.set(cache_key, result, timeout=3600)
        return Response(result)
