import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_live_updates_endpoint():
    client = APIClient()

    response = client.get(
        "/api/v1/dashboard/live-pitlines/",
    )

    assert response.status_code == 200

    body = response.json()

    assert "pit_lines" in body
