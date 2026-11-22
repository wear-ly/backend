from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "name_eng",
            "slug",
            "description",
            "description_eng",
            "brand",
            "subcategory",
            "is_active",
            "is_hidden",
        )
