import pytest
from django.urls import reverse

from categories.admin import SubcategoryInline


@pytest.mark.django_db
def test_category_detail_returns_english_name(api_client, make_variant):
    category = make_variant().product.subcategory.category
    category.name_eng = "Clothes"
    category.save(update_fields=["name_eng"])

    response = api_client.get(
        reverse("category-detail", args=[category.id]),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == 200
    assert response.data["name"] == category.name
    assert response.data["name_eng"] == "Clothes"


@pytest.mark.django_db
def test_subcategory_detail_returns_english_name(api_client, make_variant):
    assert "name_eng" in SubcategoryInline.fields
    subcategory = make_variant().product.subcategory
    subcategory.name_eng = "Shirts"
    subcategory.save(update_fields=["name_eng"])

    response = api_client.get(
        reverse("subcategory-detail", args=[subcategory.id]),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == 200
    assert response.data["name"] == subcategory.name
    assert response.data["name_eng"] == "Shirts"


@pytest.mark.django_db
def test_category_detail_returns_empty_english_name_by_default(
    api_client, make_variant
):
    category = make_variant().product.subcategory.category

    response = api_client.get(
        reverse("category-detail", args=[category.id]),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == 200
    assert response.data["name_eng"] == ""
