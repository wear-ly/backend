from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Favorite
from .serializers import FavoriteSerializer, FavoriteUserSerializer


@extend_schema_view(
    list=extend_schema(operation_id="listFavorites"),
    create=extend_schema(operation_id="createFavorite"),
    retrieve=extend_schema(operation_id="getFavorite"),
    update=extend_schema(operation_id="updateFavorite"),
    partial_update=extend_schema(operation_id="patchFavorite"),
    destroy=extend_schema(operation_id="deleteFavorite"),
)
class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Favorite.objects.none()
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(get=extend_schema(operation_id="listMyFavorites"))
class FavoriteUserListAPIView(ListAPIView):
    serializer_class = FavoriteUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Favorite.objects.none()

        return (
            Favorite.objects.filter(user=self.request.user)
            .select_related(
                "product_variant__product",
                "product_variant__size",
                "product_variant__color",
            )
            .prefetch_related("product_variant__images")
        )
