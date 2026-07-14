import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


def test_inspection_list_integration(
    client,
    inspection,
):
    response = client.get(
        "/api/v1/inspections/",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 1
    assert len(body["results"]) == 1

    item = body["results"][0]

    assert item["train_number"] == inspection.train_number
    assert item["pit_line"] == inspection.pit_line_number
    assert item["status"] == inspection.status


def test_empty_inspection_list(
    client,
):
    response = client.get(
        "/api/v1/inspections/",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["count"] == 0
    assert body["results"] == []


def test_invalid_status_filter(
    client,
):
    response = client.get(
        "/api/v1/inspections/?status=INVALID",
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Invalid inspection status.",
    }


def test_completed_status_filter(
    client,
    inspection,
):
    response = client.get(
        "/api/v1/inspections/?status=COMPLETED",
    )

    assert response.status_code == 200

    body = response.json()

    assert "results" in body
