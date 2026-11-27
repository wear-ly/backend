from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from product_images.models import ProductImage
from product_variants.models import ProductVariant

FIXTURE_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "gallery"

# filename, sort_order, try to use this file as the main photo
GALLERY_FILES = (
    ("photo.png", 0, True),
    ("detail.jpg", 1, False),
    ("clip.mp4", 2, False),
)


class Command(BaseCommand):
    help = (
        "Upload the sample gallery photo, second photo and video "
        "for one product variant to Cloudinary."
    )

    def add_arguments(self, parser):
        parser.add_argument("--sku", required=True, help="SKU of the product variant")

    def handle(self, *args, **options):
        sku = options["sku"]
        try:
            variant = ProductVariant.objects.get(sku=sku)
        except ProductVariant.DoesNotExist as exc:
            raise CommandError(
                f"Product variant with SKU {sku} was not found."
            ) from exc

        missing = [
            name for name, _, _ in GALLERY_FILES if not (FIXTURE_DIR / name).is_file()
        ]
        if missing:
            raise CommandError(f"Missing fixture files: {', '.join(missing)}")

        created = 0
        with transaction.atomic():
            has_main = ProductImage.objects.filter(
                product_variant=variant,
                is_main=True,
            ).exists()
            for filename, sort_order, wants_main in GALLERY_FILES:
                if self._already_attached(variant, filename):
                    self.stdout.write(f"Skip {filename}: already attached to {sku}")
                    continue

                is_main = wants_main and not has_main
                if wants_main and has_main:
                    self.stdout.write(
                        self.style.WARNING(
                            f"{sku} already has a main photo. {filename} was added as a regular photo."
                        )
                    )

                self._attach(variant, filename, sort_order, is_main)
                if is_main:
                    has_main = True
                created += 1
                self.stdout.write(f"Attached {filename} to {sku}")

        self.stdout.write(self.style.SUCCESS(f"Attached {created} file(s) to {sku}"))

    def _already_attached(self, variant, filename):
        stem = Path(filename).stem
        return ProductImage.objects.filter(
            product_variant=variant,
            image__icontains=f"/{stem}",
        ).exists()

    def _attach(self, variant, filename, sort_order, is_main):
        path = FIXTURE_DIR / filename
        with path.open("rb") as media_file:
            item = ProductImage(
                product_variant=variant,
                image=File(media_file, name=filename),
                is_main=is_main,
                sort_order=sort_order,
            )
            try:
                item.full_clean()
                item.save()
            except ValidationError as exc:
                raise CommandError(f"{filename}: {exc}") from exc
