from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import ProductImage
from .serializers import ProductImageSerializer


@extend_schema_view(get=extend_schema(operation_id="listProductImages"))
class ProductImageListAPIView(ListAPIView):
    queryset = ProductImage.objects.select_related("product_variant").all()
    serializer_class = ProductImageSerializer


@extend_schema_view(get=extend_schema(operation_id="getProductImage"))
class ProductImageRetrieveAPIView(RetrieveAPIView):
    queryset = ProductImage.objects.select_related("product_variant").all()
    serializer_class = ProductImageSerializer
