
from django.urls import path
from mycurrency import views

urlpatterns = [
    path('api/currency/', views.CurrencyListCreateView.as_view(), name='currency-list-create'),
    path('api/currency/<int:pk>/', views.CurrencyRetrieveUpdateDestroyView.as_view(), name='currency-detail'),
    path('api/exchange-rate/', views.CurrencyRateListView.as_view(), name='exchange-rate-list'),
    path('api/convert/', views.CurrencyConvertView.as_view(), name='currency-convert'),
]
    