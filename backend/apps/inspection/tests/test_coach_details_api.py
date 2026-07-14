import pytest

from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

def test_details_endpoint(
    inspection,
    coach,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/coaches/{coach.id}/",
    )

    assert response.status_code == 200

def test_invalid_inspection():
    client = APIClient()

    response = client.get(
        "/api/v1/inspection/11111111-1111-1111-1111-111111111111/coaches/11111111-1111-1111-1111-111111111111/",
    )

    assert response.status_code == 404

def test_invalid_coach(
    inspection,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/coaches/11111111-1111-1111-1111-111111111111/",
    )

    assert response.status_code == 404