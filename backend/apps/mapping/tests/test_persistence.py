from decimal import Decimal
from unittest.mock import Mock

from apps.mapping.contracts import ResolvedCoach
from apps.mapping.enums import TankDefectType
from apps.mapping.models import (
    CameraSide,
    CoachInspectionStatus,
    MappingStatus,
)
from apps.mapping.services.persistence import RailwayMappingPersistence


def test_create_coach_uses_repository(
    inspection,
    ntes_coach,
):
    repository = Mock()

    persistence = RailwayMappingPersistence(
        coach_repository=repository,
    )

    resolved = ResolvedCoach(
        ai_coach_number=3,
        ntes_coach=ntes_coach,
    )

    persistence.create_coach(
        inspection=inspection,
        resolved_coach=resolved,
    )

    repository.create.assert_called_once_with(
        inspection=inspection,
        resolved_coach=resolved,
        mapping_status=MappingStatus.MATCHED,
        inspection_status=CoachInspectionStatus.NORMAL,
    )


def test_create_tank_uses_repository(
    mapped_coach,
):
    repository = Mock()

    persistence = RailwayMappingPersistence(
        tank_repository=repository,
    )

    tank_data = {
        "tank_id": "L10",
        "camera_side": "left",
        "timestamp_sec": Decimal("12.500"),
        "detection_confidence": Decimal("98.50"),
        "detection_image_path": "img.png",
    }

    persistence.create_tank(
        coach=mapped_coach,
        tank_data=tank_data,
    )

    repository.create.assert_called_once_with(
        coach=mapped_coach,
        tank_identifier="L10",
        camera=CameraSide.LEFT,
        timestamp_seconds=Decimal("12.500"),
        confidence=Decimal("98.50"),
        evidence_image_path="img.png",
    )


def test_create_tank_defects_uses_repository(
    tank,
):
    repository = Mock()

    persistence = RailwayMappingPersistence(
        tank_defect_repository=repository,
    )

    persistence.create_tank_defects(
        tank=tank,
        defects=[
            TankDefectType.PIPE_NOT_CONNECTED,
        ],
        confidence=Decimal("96.20"),
    )

    repository.create_many.assert_called_once_with(
        tank=tank,
        defects=[
            TankDefectType.PIPE_NOT_CONNECTED,
        ],
        confidence=Decimal("96.20"),
    )
