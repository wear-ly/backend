from addons.cli_command_data_loader import DataLoader
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Load initial reference data"

    def handle(self, *args, **options):
        data_loader = DataLoader(self.stdout, self.style)
        data_loader.run_reference_data()

        call_command("load_terms")

        self.stdout.write(self.style.SUCCESS("Reference data loaded successfully"))
