import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_dashboard_summary():
    client = APIClient()

    response = client.get(
        "/api/dashboard/summary/",
    )

    assert response.status_code == 200

    body = response.json()

    assert "today" in body

    assert "trains_inspected" in body["today"]
    assert "bio_tanks_inspected" in body["today"]
    assert "defects_found" in body["today"]
    assert "completed_inspections" in body["today"]
