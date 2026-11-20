from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Currency
from .serializers import CurrencySerializer


@extend_schema_view(get=extend_schema(operation_id="listCurrencies"))
class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.select_related("product_variant").all()
    serializer_class = CurrencySerializer


@extend_schema_view(get=extend_schema(operation_id="getCurrency"))
class CurrencyRetrieveAPIView(RetrieveAPIView):
    queryset = Currency.objects.select_related("product_variant").all()
    serializer_class = CurrencySerializer
