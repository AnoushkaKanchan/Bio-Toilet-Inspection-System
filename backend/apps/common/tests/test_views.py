import pytest

from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_settings_endpoint():
    client = APIClient()

    response = client.get(
        "/api/v1/settings/",
    )

    assert response.status_code == 200


def test_settings_schema():
    client = APIClient()

    response = client.get(
        "/api/v1/settings/",
    )

    body = response.json()

    assert set(body.keys()) == {
        "system_status",
        "preferences",
        "about",
    }


def test_system_status_schema():
    client = APIClient()

    response = client.get(
        "/api/v1/settings/",
    )

    system = response.json()["system_status"]

    assert set(system.keys()) == {
        "overall",
        "last_updated",
        "services",
    }


def test_preferences_schema():
    client = APIClient()

    response = client.get(
        "/api/v1/settings/",
    )

    preferences = response.json()["preferences"]

    assert preferences == {
        "auto_refresh": True,
    }


def test_about_schema():
    client = APIClient()

    response = client.get(
        "/api/v1/settings/",
    )

    about = response.json()["about"]

    assert set(about.keys()) == {
        "application_name",
        "version",
        "technical_support",
    }


def test_service_count():
    client = APIClient()

    response = client.get(
        "/api/v1/settings/",
    )

    services = response.json()["system_status"]["services"]

    assert len(
        services,
    ) == 3