import os
import secrets

from django.http import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .models import Currency
from .serializers import CurrencySerializer
from .services import update_usd_exchange_rate


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.select_related("product_variant").all()
    serializer_class = CurrencySerializer


class CurrencyRetrieveAPIView(RetrieveAPIView):
    queryset = Currency.objects.select_related("product_variant").all()
    serializer_class = CurrencySerializer


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def refresh_exchange_rate(request):
    expected_token = os.getenv("EXCHANGE_RATE_UPDATE_TOKEN", "")
    provided_token = request.headers.get("X-Exchange-Token", "")

    if not expected_token or not secrets.compare_digest(provided_token, expected_token):
        return JsonResponse({"error": "Forbidden"}, status=403)

    rate = update_usd_exchange_rate()

    if rate is None:
        return JsonResponse(
            {"error": "Exchange rate update failed"},
            status=503,
        )

    return JsonResponse({"rate": str(rate)})
