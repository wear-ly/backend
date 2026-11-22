from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Product
from .serializers import ProductSerializer


@extend_schema_view(get=extend_schema(operation_id="listProducts"))
class ProductListAPIView(ListAPIView):
    queryset = Product.objects.select_related("brand", "subcategory").all()
    serializer_class = ProductSerializer


@extend_schema_view(get=extend_schema(operation_id="getProduct"))
class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.select_related("brand", "subcategory").all()
    serializer_class = ProductSerializer
