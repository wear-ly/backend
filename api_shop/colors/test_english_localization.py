import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_color_detail_returns_english_name(api_client, make_variant):
    color = make_variant().color
    assert color._meta.get_field("name_eng").verbose_name == "Name_ENG"
    color.name_eng = "Black"
    color.save(update_fields=["name_eng"])

    response = api_client.get(
        reverse("color-detail", args=[color.id]),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == 200
    assert response.data["name"] == color.name
    assert response.data["name_eng"] == "Black"


@pytest.mark.django_db
def test_color_detail_returns_empty_english_name_by_default(api_client, make_variant):
    color = make_variant().color

    response = api_client.get(
        reverse("color-detail", args=[color.id]),
        HTTP_ACCEPT="application/json",
    )

    assert response.status_code == 200
    assert response.data["name_eng"] == ""
