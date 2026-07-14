import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


def test_dashboard_endpoint(client):
    response = client.get("/api/v1/reports/dashboard/")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/json")

    body = response.json()

    assert "today" in body
    assert "weekly" in body
    assert "monthly" in body


def test_common_defects_endpoint(client):
    response = client.get(
        "/api/v1/reports/common-defects/",
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_export_daily(client):
    response = client.get(
        "/api/v1/reports/export/?type=daily",
    )

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"

    content = b"".join(
        response.streaming_content,
    )

    assert len(content) > 0


def test_export_weekly(client):
    response = client.get(
        "/api/v1/reports/export/?type=weekly",
    )

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"

    content = b"".join(
        response.streaming_content,
    )

    assert len(content) > 0


def test_export_monthly(client):
    response = client.get(
        "/api/v1/reports/export/?type=monthly",
    )

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"

    content = b"".join(
        response.streaming_content,
    )

    assert len(content) > 0
