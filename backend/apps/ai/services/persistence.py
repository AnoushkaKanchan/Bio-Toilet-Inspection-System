# apps/ai/services/persistence.py
from collections import defaultdict
from decimal import Decimal

from django.db import transaction

from apps.ai.models import AIResultRaw
from apps.ai.repositories import AIResultRawRepository
from apps.inspection.models import Inspection
from apps.inspection.repositories import InspectionRepository
from apps.mapping.contracts import ResolvedCoach
from apps.mapping.enums import TankDefectType
from apps.mapping.models import CoachInspectionStatus, MappingStatus
from apps.mapping.repositories import (
    CoachRepository,
    TankDefectRepository,
    TankRepository,
)


def _defects_for_tank(tank_data: dict) -> list[TankDefectType]:
    defects = []
    if tank_data.get("pipe_status") == "Not Connected":
        defects.append(TankDefectType.PIPE_NOT_CONNECTED)
    if tank_data.get("pipe_support_status") == "Absent":
        defects.append(TankDefectType.PIPE_SUPPORT_ABSENT)
    if tank_data.get("surface_status") == "Not Clean":
        defects.append(TankDefectType.SURFACE_NOT_CLEAN)
    return defects


class AIResultPersistenceService:

    def __init__(
        self,
        repository: AIResultRawRepository | None = None,
        coach_repository: CoachRepository | None = None,
        tank_repository: TankRepository | None = None,
        tank_defect_repository: TankDefectRepository | None = None,
        inspection_repository: InspectionRepository | None = None,
    ) -> None:
        self._repository = repository or AIResultRawRepository()
        self._coach_repository = coach_repository or CoachRepository()
        self._tank_repository = tank_repository or TankRepository()
        self._tank_defect_repository = tank_defect_repository or TankDefectRepository()
        self._inspection_repository = inspection_repository or InspectionRepository()

    @transaction.atomic
    def persist(self, *, inspection: Inspection, payload: dict) -> AIResultRaw:
        raw = self._repository.create(
            inspection=inspection,
            inspection_run_id=payload["inspection_run_id"],
            status=payload["status"],
            payload=payload,
        )
        self.persist_tanks(inspection=inspection, payload=payload)
        return raw

    @transaction.atomic
    def persist_tanks(self, *, inspection: Inspection, payload: dict) -> None:
        """
        Creates Coach/Tank/TankDefect rows from an already-validated payload.
        Split out from persist() so it can also be called standalone as a
        backfill for AIResultRaw rows that already exist but never got
        normalized (see backfill script below).
        """
        tanks_by_coach = defaultdict(list)
        for tank_data in payload.get("tanks", []):
            tanks_by_coach[tank_data["coach_number"]].append(tank_data)

        for coach_number, tank_list in tanks_by_coach.items():
            defects_by_tank = [
                (tank_data, _defects_for_tank(tank_data)) for tank_data in tank_list
            ]
            coach_has_defect = any(defects for _, defects in defects_by_tank)

            resolved_coach = ResolvedCoach(
                ai_coach_number=coach_number,
                ntes_coach=None,  # TODO: wire in real NTES matching engine
                tanks=tank_list,
            )
            coach = self._coach_repository.create(
                inspection=inspection,
                resolved_coach=resolved_coach,
                mapping_status=MappingStatus.UNMATCHED,
                inspection_status=(
                    CoachInspectionStatus.DEFECT
                    if coach_has_defect
                    else CoachInspectionStatus.NORMAL
                ),
            )

            for tank_data, defects in defects_by_tank:
                confidence = Decimal(str(tank_data["detection_confidence"]))

                tank = self._tank_repository.create(
                    coach=coach,
                    tank_identifier=tank_data["tank_id"],
                    camera=tank_data["camera_side"],  # must already be "LEFT"/"RIGHT"
                    timestamp_seconds=Decimal(str(tank_data["timestamp_sec"])),
                    confidence=confidence,
                    evidence_image_path=tank_data["tank_image_path"],
                )

                if defects:
                    self._tank_defect_repository.create_many(
                        tank=tank,
                        defects=defects,
                        confidence=confidence,
                    )

        # Refresh denormalized summary fields now that normalization is done
        statistics = self._inspection_repository.get_statistics(inspection=inspection)
        self._inspection_repository.update_summary(
            inspection=inspection,
            statistics=statistics,
        )