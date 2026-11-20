from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView, RetrieveAPIView

from categories.models import Category, Subcategory
from categories.serializers import (
    CategorySerializer,
    SubcategorySerializer,
)


@extend_schema_view(get=extend_schema(operation_id="listCategories"))
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema_view(get=extend_schema(operation_id="getCategory"))
class CategoryRetrieveAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema_view(get=extend_schema(operation_id="listSubcategories"))
class SubcategoryListAPIView(ListAPIView):
    queryset = Subcategory.objects.select_related("category")
    serializer_class = SubcategorySerializer


@extend_schema_view(get=extend_schema(operation_id="getSubcategory"))
class SubcategoryRetrieveAPIView(RetrieveAPIView):
    queryset = Subcategory.objects.select_related("category")
    serializer_class = SubcategorySerializer
