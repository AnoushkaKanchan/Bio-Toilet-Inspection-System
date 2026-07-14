import pytest

from apps.common.repositories import SettingsRepository

pytestmark = pytest.mark.django_db


def test_application_name():
    repository = SettingsRepository()

    assert (
        repository.get_application_name()
        == "AI Railway Bio-Toilet Inspection System"
    )


def test_version():
    repository = SettingsRepository()

    assert (
        repository.get_version()
        == "1.0.0 Prototype"
    )


def test_support_email():
    repository = SettingsRepository()

    assert (
        repository.get_support_email()
        == "support@example.com"
    )


def test_auto_refresh():
    repository = SettingsRepository()

    assert (
        repository.get_auto_refresh()
        is True
    )


def test_last_updated():
    repository = SettingsRepository()

    value = repository.get_last_updated()

    assert isinstance(
        value,
        str,
    )