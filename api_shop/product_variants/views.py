from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import ProductVariant
from .serializers import ProductVariantSerializer


@extend_schema_view(get=extend_schema(operation_id="listProductVariants"))
class ProductVariantListAPIView(ListAPIView):
    queryset = ProductVariant.objects.select_related("product", "size", "color").all()
    serializer_class = ProductVariantSerializer


@extend_schema_view(get=extend_schema(operation_id="getProductVariant"))
class ProductVariantRetrieveAPIView(RetrieveAPIView):
    queryset = ProductVariant.objects.select_related("product", "size", "color").all()
    serializer_class = ProductVariantSerializer
