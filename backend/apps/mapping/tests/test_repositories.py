from decimal import Decimal

import pytest

from apps.mapping.contracts import ResolvedCoach
from apps.mapping.enums import TankDefectType
from apps.mapping.models import (
    CameraSide,
    CoachInspectionStatus,
    MappingStatus,
)
from apps.mapping.repositories import (
    CoachRepository,
    TankDefectRepository,
    TankRepository,
)

pytestmark = pytest.mark.django_db


def test_create_coach(
    inspection,
    ntes_coach,
):
    repository = CoachRepository()

    resolved = ResolvedCoach(
        ai_coach_number=5,
        ntes_coach=ntes_coach,
    )

    coach = repository.create(
        inspection=inspection,
        resolved_coach=resolved,
        mapping_status=MappingStatus.MATCHED,
        inspection_status=CoachInspectionStatus.NORMAL,
    )

    assert coach.inspection == inspection
    assert coach.ntes_coach == ntes_coach
    assert coach.inspection_sequence == 5
    assert coach.mapping_status == MappingStatus.MATCHED
    assert coach.coach_inspection_status == CoachInspectionStatus.NORMAL


def test_create_tank(
    inspection,
    mapped_coach,
):
    repository = TankRepository()

    tank = repository.create(
        coach=mapped_coach,
        tank_identifier="L32",
        camera=CameraSide.LEFT,
        timestamp_seconds=Decimal("15.250"),
        confidence=Decimal("99.50"),
        evidence_image_path="evidence.png",
    )

    assert tank.coach == mapped_coach
    assert tank.tank_identifier == "L32"
    assert tank.camera == CameraSide.LEFT


def test_create_many_defects(
    tank,
):
    repository = TankDefectRepository()

    defects = repository.create_many(
        tank=tank,
        defects=[
            TankDefectType.PIPE_NOT_CONNECTED,
            TankDefectType.SURFACE_NOT_CLEAN,
        ],
        confidence=Decimal("98.10"),
    )

    assert len(defects) == 2

    assert {d.defect_type for d in defects} == {
        TankDefectType.PIPE_NOT_CONNECTED,
        TankDefectType.SURFACE_NOT_CLEAN,
    }


def test_create_many_returns_empty_for_empty_input(
    tank,
):
    repository = TankDefectRepository()

    defects = repository.create_many(
        tank=tank,
        defects=[],
        confidence=Decimal("99"),
    )

    assert defects == []
