from rest_framework import serializers
from users.serializers import UserSerializer

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("id", "user")
