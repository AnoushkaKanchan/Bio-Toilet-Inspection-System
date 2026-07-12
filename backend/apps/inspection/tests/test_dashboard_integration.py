import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


def test_dashboard_summary_endpoint(
    client,
):
    response = client.get(
        "/api/dashboard/summary/",
    )

    assert response.status_code == 200

    body = response.json()

    assert "today" in body


def test_live_pitlines_endpoint(
    client,
):
    response = client.get(
        "/api/dashboard/live-pitlines/",
    )

    assert response.status_code == 200

    body = response.json()

    assert "pit_lines" in body


def test_operations_status_endpoint(
    client,
):
    response = client.get(
        "/api/dashboard/status/",
    )

    assert response.status_code == 200

    body = response.json()

    assert "status" in body
    assert "message" in body


def test_recent_activity_endpoint(
    client,
):
    response = client.get(
        "/api/dashboard/recent-activity/",
    )

    assert response.status_code == 200

    body = response.json()

    assert "activities" in body


def test_train_mapping_endpoint(
    client,
    inspection,
):
    response = client.get(
        f"/api/dashboard/train-mapping/{inspection.id}/",
    )

    assert response.status_code == 200

    body = response.json()

    assert "inspection_id" in body
    assert "train_number" in body
    assert "coaches" in body
