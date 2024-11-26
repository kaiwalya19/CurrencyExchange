from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Currency, CurrencyExchangeRate
from .adapters import  CurrencyBeaconProvider, MockProvider

# Define a custom form for the admin converter view
class CurrencyConverterForm(forms.Form):
    source_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), label="Source Currency")
    target_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), label="Target Currency")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount to Convert")

# Custom admin view for currency conversion
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol')
    change_list_template = "admin/currency_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('convert/', self.admin_site.admin_view(self.convert_view), name="currency_convert"),
        ]
        return custom_urls + urls

    def convert_view(self, request):
        if request.method == 'POST':
            form = CurrencyConverterForm(request.POST)
            if form.is_valid():
                source_currency = form.cleaned_data['source_currency']
                target_currency = form.cleaned_data['target_currency']
                amount = form.cleaned_data['amount']

                # Fetch exchange rate using adapters
                provider = CurrencyBeaconProvider()  # Replace with your primary provider
                rate_data = provider.get_exchange_rate_data(source_currency.code, target_currency.code)
                if rate_data:
                    converted_amount = float(amount) * float(rate_data['rate_value'])
                    self.message_user(request, f"Converted Amount: {converted_amount:.2f} {target_currency.code}")
                else:
                    self.message_user(request, "Exchange rate not found.", level="error")
                return HttpResponseRedirect(request.path)
        else:
            form = CurrencyConverterForm()

        context = {
            'form': form,
            'title': "Convert Currency",
        }
        return render(request, "admin/currency_convert.html", context)

# Register the model with the custom admin class
admin.site.register(Currency, CurrencyAdmin)

@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('source_currency', 'exchanged_currency', 'valuation_date', 'rate_value')
