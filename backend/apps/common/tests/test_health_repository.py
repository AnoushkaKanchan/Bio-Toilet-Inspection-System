import pytest

from apps.common.health_repository import (
    HealthRepository,
)

pytestmark = pytest.mark.django_db


def test_database_online():
    repository = HealthRepository()

    assert (
        repository.is_database_online()
        is True
    )


def test_timestamp():
    repository = HealthRepository()

    assert isinstance(
        repository.get_timestamp(),
        str,
    )