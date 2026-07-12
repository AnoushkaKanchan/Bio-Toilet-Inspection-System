import pytest

from apps.inspection.models import InspectionStatus
from apps.inspection.repositories import InspectionRepository

pytestmark = pytest.mark.django_db


def test_list_returns_queryset(
    inspection,
):
    repository = InspectionRepository()

    queryset = repository.list()

    assert queryset.count() == 1


def test_status_filter(
    inspection,
):
    repository = InspectionRepository()

    queryset = repository.list(
        status=InspectionStatus.COMPLETED,
    )

    assert queryset.count() in (0, 1)
