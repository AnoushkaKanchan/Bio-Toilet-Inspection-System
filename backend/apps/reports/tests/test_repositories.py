from datetime import timedelta

import pytest
from django.utils import timezone

from apps.inspection.models import (
    Inspection,
    InspectionStatus,
)
from apps.mapping.models import (
    CameraSide,
    Coach,
    CoachInspectionStatus,
    MappingStatus,
    Tank,
    TankDefect,
)
from apps.reports.repositories import ReportsRepository

pytestmark = pytest.mark.django_db


@pytest.fixture
def repository():
    return ReportsRepository()


@pytest.fixture
def inspection():
    return Inspection.objects.create(
        train_number="12951",
        pit_line_number="P1",
        inspection_time=timezone.now(),
        status=InspectionStatus.COMPLETED,
    )


@pytest.fixture
def coach(inspection):
    return Coach.objects.create(
        inspection=inspection,
        inspection_sequence=0,
        mapping_status=MappingStatus.MATCHED,
        coach_inspection_status=CoachInspectionStatus.NORMAL,
    )


@pytest.fixture
def tank(coach):
    return Tank.objects.create(
        coach=coach,
        tank_identifier="L1",
        camera=CameraSide.LEFT,
        timestamp_seconds=1,
        confidence=99,
        evidence_image_path="tank.jpg",
    )


@pytest.fixture
def defect(tank):
    return TankDefect.objects.create(
        tank=tank,
        defect_type="PIPE_NOT_CONNECTED",
        confidence=98,
    )


def test_today_summary(
    repository,
    inspection,
    coach,
    tank,
    defect,
):
    summary = repository.get_today_summary()

    assert summary.trains_inspected == 1
    assert summary.bio_tanks_inspected == 1
    assert summary.defects_found == 1
    assert summary.completed == 1


def test_weekly_summary(
    repository,
    inspection,
    coach,
    tank,
    defect,
):
    summary = repository.get_weekly_summary()

    assert summary.trains_inspected == 1
    assert summary.coaches_inspected == 1
    assert summary.bio_tanks_inspected == 1
    assert summary.total_defects == 1


def test_monthly_summary(
    repository,
    inspection,
    coach,
    tank,
    defect,
):
    summary = repository.get_monthly_summary()

    assert summary.trains_inspected == 1
    assert summary.coaches_inspected == 1
    assert summary.bio_tanks_inspected == 1
    assert summary.total_defects == 1


def test_common_defects(
    repository,
    inspection,
    coach,
    tank,
):
    TankDefect.objects.create(
        tank=tank,
        defect_type="PIPE_NOT_CONNECTED",
        confidence=90,
    )

    another_tank = Tank.objects.create(
        coach=coach,
        tank_identifier="R1",
        camera=CameraSide.RIGHT,
        timestamp_seconds=2,
        confidence=95,
        evidence_image_path="tank2.jpg",
    )

    TankDefect.objects.create(
        tank=another_tank,
        defect_type="PIPE_NOT_CONNECTED",
        confidence=88,
    )

    defects = repository.get_common_defects()

    assert len(defects) == 1
    assert defects[0].defect_type == "PIPE_NOT_CONNECTED"
    assert defects[0].display_name == "Pipe Not Connected"
    assert defects[0].count == 2


def test_weekly_summary_excludes_old_data(
    repository,
):
    old = Inspection.objects.create(
        train_number="12951",
        pit_line_number="P1",
        inspection_time=timezone.now(),
        status=InspectionStatus.COMPLETED,
    )

    Inspection.objects.filter(
        id=old.id,
    ).update(
        created_at=timezone.now() - timedelta(days=10),
    )

    summary = repository.get_weekly_summary()

    assert summary.trains_inspected == 0


def test_monthly_summary_excludes_old_data(
    repository,
):
    old = Inspection.objects.create(
        train_number="12951",
        pit_line_number="P1",
        inspection_time=timezone.now(),
        status=InspectionStatus.COMPLETED,
    )

    Inspection.objects.filter(
        id=old.id,
    ).update(
        created_at=timezone.now() - timedelta(days=40),
    )

    summary = repository.get_monthly_summary()

    assert summary.trains_inspected == 0


def test_empty_common_defects(
    repository,
):
    assert repository.get_common_defects() == []
