import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_list_endpoint(
    inspection,
):
    client = APIClient()

    response = client.get(
        "/api/inspections/",
    )

    assert response.status_code == 200

    body = response.json()

    assert "count" in body
    assert "results" in body


def test_invalid_status():
    client = APIClient()

    response = client.get(
        "/api/inspections/?status=INVALID",
    )

    assert response.status_code == 400


def test_status_filter(
    inspection,
):
    client = APIClient()

    response = client.get(
        "/api/inspections/?status=COMPLETED",
    )

    assert response.status_code == 200
