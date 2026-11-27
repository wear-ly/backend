from django.contrib import admin

from .models import Currency, ExchangeRate
from .services import update_usd_exchange_rate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_variant",
        "currency_code",
        "amount",
    )
    search_fields = (
        "currency_code",
        "product_variant__sku",
    )
    list_filter = ("currency_code",)
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("product_variant",)

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("from_currency", "to_currency", "rate", "updated_at")

    actions = ["refresh_rate"]

    @admin.action(description="Оновити курс із Monobank")
    def refresh_rate(self, request, queryset):
        rate = update_usd_exchange_rate()

        if rate is not None:
            self.message_user(request, f"Курс USD/UAH оновлено: {rate}")
        else:
            self.message_user(
                request,
                "Не вдалося отримати курс. Попереднє значення збережено.",
                level="error",
            )
