from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Discount
from .serializers import DiscountSerializer


@extend_schema_view(get=extend_schema(operation_id="listDiscounts"))
class DiscountListAPIView(ListAPIView):
    queryset = Discount.objects.select_related("product_variant").all()
    serializer_class = DiscountSerializer


@extend_schema_view(get=extend_schema(operation_id="getDiscount"))
class DiscountRetrieveAPIView(RetrieveAPIView):
    queryset = Discount.objects.select_related("product_variant").all()
    serializer_class = DiscountSerializer
