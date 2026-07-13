import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_coach_list_endpoint(
    inspection,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/coaches/",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["inspection_id"] == str(
        inspection.id,
    )

    assert body["train_number"] == inspection.train_number

    assert body["train_name"] == inspection.train_name

    assert "coaches" in body


def test_invalid_filter(
    inspection,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/coaches/?filter=INVALID",
    )

    assert response.status_code == 400


def test_invalid_inspection():
    client = APIClient()

    response = client.get(
        "/api/v1/inspection/11111111-1111-1111-1111-111111111111/coaches/",
    )

    assert response.status_code == 404