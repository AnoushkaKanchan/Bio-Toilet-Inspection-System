import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_dashboard_status_endpoint():
    client = APIClient()

    response = client.get(
        "/api/dashboard/status/",
    )

    assert response.status_code == 200

    body = response.json()

    assert "status" in body
    assert "message" in body
