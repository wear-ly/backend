from currencies.services import update_usd_exchange_rate
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update USD/UAH exchange rate from Monobank"

    def handle(self, *args, **options):
        rate = update_usd_exchange_rate()

        if rate is None:
            self.stdout.write(
                self.style.WARNING("Monobank unavailable. Previous rate preserved.")
            )
            return

        self.stdout.write(self.style.SUCCESS(f"USD/UAH exchange rate updated: {rate}"))
