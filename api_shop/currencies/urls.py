from django.urls import path

from .views import (
    CurrencyListAPIView,
    CurrencyRetrieveAPIView,
    refresh_exchange_rate,
)

urlpatterns = [
    path("", CurrencyListAPIView.as_view(), name="currency-list"),
    path(
        "refresh-exchange-rate/",
        refresh_exchange_rate,
        name="refresh-exchange-rate",
    ),
    path("<int:pk>/", CurrencyRetrieveAPIView.as_view(), name="currency-detail"),
]
