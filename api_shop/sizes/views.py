from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Size
from .serializers import SizeSerializer


@extend_schema_view(get=extend_schema(operation_id="listSizes"))
class SizeListAPIView(ListAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


@extend_schema_view(get=extend_schema(operation_id="getSize"))
class SizeRetrieveAPIView(RetrieveAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
