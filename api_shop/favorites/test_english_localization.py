import pytest
from django.urls import reverse

from favorites.models import Favorite


@pytest.mark.django_db
def test_favorite_list_returns_english_product_title(api_client, user, make_variant):
    variant = make_variant()
    variant.product.name_eng = "English shirt"
    variant.product.save(update_fields=["name_eng"])
    Favorite.objects.create(user=user, product_variant=variant)

    response = api_client.get(
        reverse("favorite-user-list"),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == 200
    item = response.data["results"][0]["product_variant"]
    assert item["product_title"] == variant.product.name
    assert item["product_title_eng"] == "English shirt"


@pytest.mark.django_db
def test_favorite_list_returns_empty_english_title_by_default(
    api_client, user, make_variant
):
    variant = make_variant()
    Favorite.objects.create(user=user, product_variant=variant)

    response = api_client.get(
        reverse("favorite-user-list"),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == 200
    item = response.data["results"][0]["product_variant"]
    assert item["product_title_eng"] == ""
