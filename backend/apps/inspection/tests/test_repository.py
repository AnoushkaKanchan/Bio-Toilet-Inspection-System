from decimal import Decimal
import pytest

from apps.inspection.models import Inspection
from apps.inspection.repositories import InspectionRepository
from apps.mapping.models import (
    CameraSide,
    Coach,
    Tank,
    TankDefect,
    Coach,
)

pytestmark = pytest.mark.django_db


def test_get_details_returns_correct_inspection(
    inspection,
):
    repository = InspectionRepository()

    # Act
    result = repository.get_details(
        inspection_id=inspection.id,
    )

    # Assert
    assert isinstance(result, Inspection)
    assert result.id == inspection.id


def test_get_details_raises_does_not_exist():
    repository = InspectionRepository()

    # Assert that lookups with non-existent IDs cleanly bubble up Django's DoesNotExist exception
    with pytest.raises(Inspection.DoesNotExist):
        repository.get_details(
            inspection_id=9999,
        )


def test_get_defect_summary(
    inspection,
):
    repository = InspectionRepository()

    coach = Coach.objects.create(
        inspection=inspection,
        inspection_sequence=1,
    )

    tank = Tank.objects.create(
        coach=coach,
        tank_identifier="L1",
        camera=CameraSide.LEFT,
        timestamp_seconds=Decimal("0.000"),
        confidence=Decimal("99.00"),
    )

    TankDefect.objects.create(
        tank=tank,
        defect_type="PIPE_NOT_CONNECTED",
        confidence=Decimal("95.00"),
    )

    summary = repository.get_defect_summary(
        inspection=inspection,
    )

    assert len(summary) == 1
    assert summary[0]["defect_type"] == "PIPE_NOT_CONNECTED"
    assert summary[0]["count"] == 1