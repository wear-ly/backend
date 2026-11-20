from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Brand
from .serializers import BrandSerializer


@extend_schema_view(get=extend_schema(operation_id="listBrands"))
class BrandListAPIView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


@extend_schema_view(get=extend_schema(operation_id="getBrand"))
class BrandRetrieveAPIView(RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
