from addons.mixins import TimeStampMixin
from addons.slugify import generate_unique_slug
from django.db import models


class Category(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()

        if not self.slug:
            self.slug = generate_unique_slug(Category, self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-created_at"]


class Subcategory(TimeStampMixin):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
    )

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()

        if not self.slug:
            self.slug = generate_unique_slug(Subcategory, self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
        ordering = ["-created_at"]
