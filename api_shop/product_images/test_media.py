import pytest
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient

from product_images.models import MediaType, ProductImage
from product_images.serializers import ProductImagesForFavoriteSerializer

pytestmark = pytest.mark.django_db

IMAGE_MAX_BYTES = 8 * 1024 * 1024


@pytest.fixture
def local_media(tmp_path):
    field = ProductImage._meta.get_field("image")
    original = field.storage
    field.storage = FileSystemStorage(location=tmp_path)
    yield
    field.storage = original


def uploaded(name, content=b"file-bytes"):
    return SimpleUploadedFile(name, content)


def test_png_is_stored_as_image(make_variant, local_media):
    item = ProductImage(
        product_variant=make_variant(),
        image=uploaded("front.png"),
        is_main=True,
        sort_order=0,
    )

    item.save()
    item.refresh_from_db()

    assert item.media_type == MediaType.IMAGE
    assert "/image/" in item.image.name


def test_mp4_is_stored_as_video(make_variant, local_media):
    item = ProductImage(
        product_variant=make_variant(),
        image=uploaded("clip.mp4"),
        is_main=False,
        sort_order=2,
    )

    item.save()
    item.refresh_from_db()

    assert item.media_type == MediaType.VIDEO
    assert "/video/" in item.image.name


def test_video_cannot_be_the_main_photo(make_variant, local_media):
    item = ProductImage(
        product_variant=make_variant(),
        image=uploaded("clip.mp4"),
        is_main=True,
    )

    with pytest.raises(ValidationError):
        item.save()


def test_gif_is_rejected(make_variant, local_media):
    item = ProductImage(
        product_variant=make_variant(),
        image=uploaded("anim.gif"),
        is_main=False,
    )

    with pytest.raises(ValidationError):
        item.save()


def test_photo_over_8mb_is_rejected(make_variant, local_media):
    item = ProductImage(
        product_variant=make_variant(),
        image=uploaded("huge.png", b"x" * (IMAGE_MAX_BYTES + 1)),
        is_main=False,
    )

    with pytest.raises(ValidationError):
        item.save()


def test_list_returns_media_type_and_image(make_variant, local_media):
    variant = make_variant()
    ProductImage(
        product_variant=variant,
        image=uploaded("front.png"),
        is_main=True,
    ).save()

    response = APIClient().get(
        reverse("product-image-list"),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == 200
    payload = response.json()
    rows = payload["results"] if isinstance(payload, dict) else payload
    row = next(item for item in rows if item["product_variant"] == variant.id)
    assert row["media_type"] == MediaType.IMAGE
    assert row["image"]


def test_favorite_serializer_includes_media_type(make_variant, local_media):
    item = ProductImage(
        product_variant=make_variant(),
        image=uploaded("front.png"),
        is_main=True,
    )
    item.save()

    data = ProductImagesForFavoriteSerializer(item).data

    assert data["media_type"] == MediaType.IMAGE
    assert data["image"]
