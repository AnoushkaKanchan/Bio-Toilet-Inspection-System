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


class RailwayMappingPersistence:
    """
    Persists railway mapping domain entities.
    """

    def create_coach(
        self,
        *,
        inspection: Inspection,
        resolved_coach: ResolvedCoach,
    ) -> Coach:
        return Coach.objects.create(
            inspection=inspection,
            ntes_coach=resolved_coach.ntes_coach,
            inspection_sequence=resolved_coach.ai_coach_number,
            mapping_status=self._initial_mapping_status(),
            coach_inspection_status=self._initial_inspection_status(),
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
        evidence_image_path = tank_data["detection_image_path"]

        return Tank.objects.create(
            coach=coach,
            tank_identifier=tank_identifier,
            camera=self._camera_side(camera),
            timestamp_seconds=timestamp,
            confidence=confidence,
            evidence_image_path=evidence_image_path,
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

    def create_tank_defects(
        self,
        *,
        tank: Tank,
        defects: list[TankDefectType],
        confidence: Decimal,
    ) -> list[TankDefect]:
        if not defects:
            return []

        created_defects = []

        for defect in defects:
            created_defects.append(
                TankDefect.objects.create(
                    tank=tank,
                    defect_type=defect,
                    confidence=confidence,
                )
            )

        return created_defects
