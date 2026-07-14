import pytest

from apps.common.dto import (
    SystemStatusDTO,
)
from apps.common.services import (
    HealthService,
)

pytestmark = pytest.mark.django_db


def test_get_system_status():
    service = HealthService()

    status = service.get_system_status()

    assert isinstance(
        status,
        SystemStatusDTO,
    )


def test_overall_status():
    service = HealthService()

    status = service.get_system_status()

    assert status.overall == "ONLINE"


def test_services():
    service = HealthService()

    status = service.get_system_status()

    assert len(status.services) == 4

    assert status.services[0].status == "UNKNOWN"
    assert status.services[1].status == "UNKNOWN"
    assert status.services[2].status == "ONLINE"
    assert status.services[3].status == "ONLINE"