from decimal import Decimal

from apps.inspection.models import Inspection
from apps.mapping.contracts import ResolvedCoach
from apps.mapping.enums import TankDefectType
from apps.mapping.models import (
    CameraSide,
    Coach,
    CoachInspectionStatus,
    MappingStatus,
    Tank,
    TankDefect,
)
from apps.mapping.repositories import (
    CoachRepository,
    TankDefectRepository,
    TankRepository,
)


class RailwayMappingPersistence:

    def __init__(
        self,
        *,
        coach_repository: CoachRepository | None = None,
        tank_repository: TankRepository | None = None,
        tank_defect_repository: TankDefectRepository | None = None,
    ) -> None:
        self._coach_repository = coach_repository or CoachRepository()
        self._tank_repository = tank_repository or TankRepository()
        self._tank_defect_repository = tank_defect_repository or TankDefectRepository()

    def create_coach(
        self,
        *,
        inspection: Inspection,
        resolved_coach: ResolvedCoach,
    ) -> Coach:
        return self._coach_repository.create(
            inspection=inspection,
            resolved_coach=resolved_coach,
            mapping_status=self._initial_mapping_status(),
            inspection_status=self._initial_inspection_status(),
        )

    def create_tank(
        self,
        *,
        coach: Coach,
        tank_data: dict,
    ) -> Tank:
        tank_identifier = tank_data["tank_id"]
        camera = tank_data["camera_side"]
        timestamp = tank_data["timestamp_sec"]
        confidence = tank_data["detection_confidence"]
        # apps/mapping/services/persistence.py, create_tank()
        evidence_image_path = tank_data["tank_image_path"]
        
        return self._tank_repository.create(
            coach=coach,
            tank_identifier=tank_identifier,
            camera=self._camera_side(camera),
            timestamp_seconds=timestamp,
            confidence=confidence,
            evidence_image_path=evidence_image_path,
        )

    def create_tank_defects(
        self,
        *,
        tank: Tank,
        defects: list[TankDefectType],
        confidence: Decimal,
    ) -> list[TankDefect]:
        return self._tank_defect_repository.create_many(
            tank=tank,
            defects=defects,
            confidence=confidence,
        )

    def _initial_mapping_status(
        self,
    ) -> MappingStatus:
        return MappingStatus.MATCHED

    def _initial_inspection_status(
        self,
    ) -> CoachInspectionStatus:
        return CoachInspectionStatus.NORMAL

    def _camera_side(
        self,
        value: str,
    ) -> CameraSide:
        return CameraSide[value.upper()]
    
    def clear_mapping(
        self,
        *,
        inspection: Inspection,
    ) -> None:
        self._coach_repository.delete_by_inspection(
            inspection=inspection,
        )