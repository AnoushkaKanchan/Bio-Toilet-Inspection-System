import pytest

from apps.common.dto import (
    SettingsDTO,
)
from apps.common.services import (
    SettingsService,
)

pytestmark = pytest.mark.django_db


def test_get_settings():
    service = SettingsService()

    settings = service.get_settings()

    assert isinstance(
        settings,
        SettingsDTO,
    )


def test_preferences():
    service = SettingsService()

    settings = service.get_settings()

    assert (
        settings.preferences.auto_refresh
        is True
    )


def test_about():
    service = SettingsService()

    settings = service.get_settings()

    assert (
        settings.about.application_name
        == "AI Railway Bio-Toilet Inspection System"
    )

    assert (
        settings.about.version
        == "1.0.0 Prototype"
    )


def test_support():
    service = SettingsService()

    settings = service.get_settings()

    assert (
        settings.about.technical_support.email
        == "support@example.com"
    )