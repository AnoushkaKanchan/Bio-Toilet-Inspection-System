import pytest

from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

def test_report_schema(
    inspection,
    coach,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/coaches/{coach.id}/",
    )

    assert response.status_code == 200

    body = response.json()

    assert set(body.keys()) == {
        "coach",
        "inspection",
        "health_diagram",
        "findings",
        "maintenance",
        "remarks",
        "navigation",
    }

def test_navigation_schema(
    inspection,
    coach,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/coaches/{coach.id}/",
    )

    body = response.json()

    assert "previous" in body["navigation"]
    assert "next" in body["navigation"]

def test_health_diagram_schema(
    inspection,
    coach,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/coaches/{coach.id}/",
    )

    diagram = response.json()["health_diagram"]

    assert set(diagram.keys()) == {
        "front_left",
        "front_right",
        "rear_left",
        "rear_right",
        "bio_tank",
    }

