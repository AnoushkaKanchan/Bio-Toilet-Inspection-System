from decimal import Decimal

from django.db.models import QuerySet

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


class CoachRepository:
    def create(
        self,
        *,
        inspection: Inspection,
        resolved_coach: ResolvedCoach,
        mapping_status: MappingStatus,
        inspection_status: CoachInspectionStatus,
    ) -> Coach:
        return Coach.objects.create(
            inspection=inspection,
            ntes_coach=resolved_coach.ntes_coach,
            inspection_sequence=resolved_coach.ai_coach_number,
            mapping_status=mapping_status,
            coach_inspection_status=inspection_status,
        )

    def get_by_inspection(
        self,
        *,
        inspection,
    ) -> list[Coach]:
        return list(
            Coach.objects.filter(
                inspection=inspection,
            ).order_by(
                "inspection_sequence",
            )
        )

    def get_detailed_by_inspection(
        self,
        *,
        inspection: Inspection,
    ) -> QuerySet:
        return (
            Coach.objects.filter(
                inspection=inspection,
            )
            .select_related(
                "ntes_coach",
            )
            .prefetch_related(
                "tanks__defects",
            )
            .order_by(
                "inspection_sequence",
            )
        )
    
    def get_details(
        self,
        *,
        inspection: Inspection,
        coach_id,
    ) -> Coach:
        return (
            Coach.objects
            .select_related(
                "ntes_coach",
            )
            .prefetch_related(
                "tanks__defects",
            )
            .get(
                inspection=inspection,
                id=coach_id,
            )
        )
    
    def get_previous_coach(
        self,
        *,
        inspection: Inspection,
        coach: Coach,
    ) -> Coach | None:
        return (
            Coach.objects.filter(
                inspection=inspection,
                inspection_sequence__lt=coach.inspection_sequence,
            )
            .order_by(
                "-inspection_sequence",
            )
            .first()
        )

    def get_next_coach(
        self,
        *,
        inspection: Inspection,
        coach: Coach,
    ) -> Coach | None:
        return (
            Coach.objects.filter(
                inspection=inspection,
                inspection_sequence__gt=coach.inspection_sequence,
            )
            .order_by(
                "inspection_sequence",
            )
            .first()
        )

class TankRepository:
    def create(
        self,
        *,
        coach: Coach,
        tank_identifier: str,
        camera: CameraSide,
        timestamp_seconds: Decimal,
        confidence: Decimal,
        evidence_image_path: str,
    ) -> Tank:
        return Tank.objects.create(
            coach=coach,
            tank_identifier=tank_identifier,
            camera=camera,
            timestamp_seconds=timestamp_seconds,
            confidence=confidence,
            evidence_image_path=evidence_image_path,
        )


class TankDefectRepository:
    def create_many(
        self,
        *,
        tank: Tank,
        defects: list[TankDefectType],
        confidence: Decimal,
    ) -> list[TankDefect]:
        created = []

        for defect in defects:
            created.append(
                TankDefect.objects.create(
                    tank=tank,
                    defect_type=defect,
                    confidence=confidence,
                )
            )

        return created
