import requests
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from currencies.models import ExchangeRate
from currencies.services import update_usd_exchange_rate


class ExchangeRateTests(TestCase):

    @patch("currencies.services.requests.get")
    def test_exchange_rate_saved_to_database(self, mock_get):
        mock_get.return_value.json.return_value = [
            {
                "currencyCodeA": 840,
                "currencyCodeB": 980,
                "rateSell": 45.86,
            }
        ]

        rate = update_usd_exchange_rate()

        saved_rate = ExchangeRate.objects.get(
            from_currency="USD",
            to_currency="UAH",
        )

        self.assertEqual(rate, Decimal("45.86"))
        self.assertEqual(saved_rate.rate, Decimal("45.86"))

    @patch("currencies.services.requests.get")
    def test_previous_rate_preserved_on_api_error(self, mock_get):
        ExchangeRate.objects.create(
            from_currency="USD",
            to_currency="UAH",
            rate=Decimal("45.86"),
        )

        mock_get.side_effect = requests.RequestException(
            "Monobank unavailable"
        )

        result = update_usd_exchange_rate()

        saved_rate = ExchangeRate.objects.get(
            from_currency="USD",
            to_currency="UAH",
        )

        self.assertIsNone(result)
        self.assertEqual(saved_rate.rate, Decimal("45.86"))


class ExchangeRateEndpointTests(TestCase):

    def test_missing_token_returns_403(self):
        with patch.dict("os.environ", {"EXCHANGE_RATE_UPDATE_TOKEN": "test-secret"}):
            response = self.client.post("/api/currencies/refresh-exchange-rate/")
        self.assertEqual(response.status_code, 403)

    def test_invalid_token_returns_403(self):
        with patch.dict("os.environ", {"EXCHANGE_RATE_UPDATE_TOKEN": "test-secret"}):
            response = self.client.post(
                "/api/currencies/refresh-exchange-rate/",
                HTTP_X_EXCHANGE_TOKEN="wrong-token",
            )
        self.assertEqual(response.status_code, 403)

    @patch("currencies.views.update_usd_exchange_rate")
    def test_valid_token_returns_200(self, mock_update):
        mock_update.return_value = Decimal("45.86")

        with patch.dict("os.environ", {"EXCHANGE_RATE_UPDATE_TOKEN": "test-secret"}):
            response = self.client.post(
                "/api/currencies/refresh-exchange-rate/",
                HTTP_X_EXCHANGE_TOKEN="test-secret",
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["rate"], "45.86")
        mock_update.assert_called_once()
