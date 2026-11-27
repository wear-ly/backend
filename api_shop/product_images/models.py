from addons.mixins import TimeStampMixin
from django.core.exceptions import ValidationError
from django.db import models
from product_variants.models import ProductVariant

from .storage import ProductMediaStorage
from .utils import (
    ALLOWED_EXTENSIONS,
    IMAGE_MAX_BYTES,
    VIDEO_MAX_BYTES,
    file_extension,
    media_kind_for_filename,
    product_image_upload_path,
)


class MediaType(models.TextChoices):
    IMAGE = "image", "Image"
    VIDEO = "video", "Video"


class ProductImage(TimeStampMixin):
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.FileField(
        upload_to=product_image_upload_path,
        storage=ProductMediaStorage(),
    )

    media_type = models.CharField(
        max_length=10,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
    )

    is_main = models.BooleanField(
        default=False,
    )

    sort_order = models.PositiveIntegerField(
        default=0,
    )

    def __str__(self):
        return f"{self.product_variant.sku} {self.media_type}"

    def clean(self):
        super().clean()
        self._prepare_upload()

    def save(self, *args, **kwargs):
        self._prepare_upload()
        super().save(*args, **kwargs)

    def _prepare_upload(self):
        image = self.image
        if not image or getattr(image, "_committed", True):
            self._reject_main_video()
            return

        extension = file_extension(image.name)
        if extension not in ALLOWED_EXTENSIONS:
            raise ValidationError(
                {"image": "Allowed files: jpg, jpeg, png, webp, mp4, webm."}
            )

        self.media_type = media_kind_for_filename(image.name)
        limit = (
            VIDEO_MAX_BYTES if self.media_type == MediaType.VIDEO else IMAGE_MAX_BYTES
        )
        if image.size > limit:
            raise ValidationError({"image": "File is too large."})
        self._reject_main_video()

    def _reject_main_video(self):
        if self.media_type == MediaType.VIDEO and self.is_main:
            raise ValidationError({"is_main": "A video cannot be the main photo."})

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ["sort_order", "id"]

        indexes = [
            models.Index(fields=["product_variant"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["product_variant"],
                condition=models.Q(is_main=True),
                name="unique_main_image_per_product_variant",
            ),
        ]
