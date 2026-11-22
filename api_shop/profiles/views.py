from api_shop.permissions import IsOwner
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from profiles.models import Profile
from profiles.serializers import ProfileSerializer


@extend_schema_view(
    list=extend_schema(operation_id="listProfiles"),
    retrieve=extend_schema(operation_id="getProfile"),
    update=extend_schema(operation_id="updateProfile"),
    partial_update=extend_schema(operation_id="patchProfile"),
)
class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_url_kwarg = "profile_id"
    http_method_names = ["get", "put", "patch"]

    def get_queryset(self):
        return super().get_queryset().exclude(user__is_staff=True)
