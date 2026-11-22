from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Color
from .serializers import ColorSerializer


@extend_schema_view(get=extend_schema(operation_id="listColors"))
class ColorListAPIView(ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


@extend_schema_view(get=extend_schema(operation_id="getColor"))
class ColorRetrieveAPIView(RetrieveAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
