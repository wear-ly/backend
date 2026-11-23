import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_product_detail_returns_filled_english_fields(api_client, make_variant):
    product = make_variant().product
    assert product._meta.get_field("name_eng").verbose_name == "Name_ENG"
    assert product._meta.get_field("description_eng").verbose_name == "Description_ENG"
    product.name_eng = "Linen shirt"
    product.description_eng = "Light summer shirt"
    product.save(update_fields=["name_eng", "description_eng"])

    response = api_client.get(
        reverse("product-detail", args=[product.id]),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == 200
    assert response.data["name"] == product.name
    assert response.data["description"] == product.description
    assert response.data["name_eng"] == "Linen shirt"
    assert response.data["description_eng"] == "Light summer shirt"


@pytest.mark.django_db
def test_product_detail_returns_empty_english_fields_by_default(
    api_client, make_variant
):
    product = make_variant().product

    response = api_client.get(
        reverse("product-detail", args=[product.id]),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == 200
    assert response.data["name_eng"] == ""
    assert response.data["description_eng"] == ""
