import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_recent_activity_endpoint():
    client = APIClient()

    response = client.get(
        "/api/dashboard/recent-activity/",
    )

    assert response.status_code == 200

    body = response.json()

    assert "activities" in body
