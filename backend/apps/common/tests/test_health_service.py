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

    assert len(
        status.services,
    ) == 3

    assert status.services[0].name == "AI Inference Engine"

    assert status.services[1].name == "Camera Network"

    assert status.services[2].name == "Backend Connection"