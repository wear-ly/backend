from django.contrib import admin

from .models import ProductImage


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_variant",
        "media_type",
        "is_main",
        "sort_order",
    )
    search_fields = ("product_variant__sku",)
    list_filter = ("is_main", "media_type")
    readonly_fields = ("created_at", "updated_at", "media_type")
    list_select_related = ("product_variant",)
