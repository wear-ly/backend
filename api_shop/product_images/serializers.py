from rest_framework import serializers

from .models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id",
            "product_variant",
            "image",
            "media_type",
            "is_main",
            "sort_order",
        )
        read_only_fields = ("media_type",)


class ProductImagesForFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image",
            "media_type",
            "is_main",
            "sort_order",
        )
        read_only_fields = ("media_type",)
