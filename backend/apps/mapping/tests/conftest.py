from decimal import Decimal

import pytest
from django.utils import timezone

from apps.inspection.models import Inspection
from apps.mapping.models import (
    CameraSide,
    Coach,
    CoachInspectionStatus,
    MappingStatus,
    Tank,
)
from apps.ntes.models import NTESCoach


@pytest.fixture
def inspection(db):
    return Inspection.objects.create(
        train_number="12951",
        pit_line_number="P1",
        inspection_time=timezone.now(),
    )


@pytest.fixture
def ntes_coach(db, inspection):
    return NTESCoach.objects.create(
        inspection=inspection,
        coach_sequence=0,
        coach_number="ENG",
        coach_type="ENG",
    )


@pytest.fixture
def mapped_coach(
    db,
    inspection,
    ntes_coach,
):
    return Coach.objects.create(
        inspection=inspection,
        ntes_coach=ntes_coach,
        inspection_sequence=1,
        mapping_status=MappingStatus.MATCHED,
        coach_inspection_status=CoachInspectionStatus.NORMAL,
    )


@pytest.fixture
def tank(
    db,
    mapped_coach,
):
    return Tank.objects.create(
        coach=mapped_coach,
        tank_identifier="L32",
        camera=CameraSide.LEFT,
        timestamp_seconds=Decimal("10.000"),
        confidence=Decimal("99.90"),
        evidence_image_path="evidence.png",
    )
@pytest.fixture
def coach(
    inspection,
):
    return Coach.objects.create(
        inspection=inspection,
        inspection_sequence=1,
        mapping_status=MappingStatus.MATCHED,
        coach_inspection_status=CoachInspectionStatus.NORMAL,
    )

@pytest.fixture
def coach(
    inspection,
):
    return Coach.objects.create(
        inspection=inspection,
        inspection_sequence=1,
        mapping_status=MappingStatus.MATCHED,
        coach_inspection_status=CoachInspectionStatus.NORMAL,
    )