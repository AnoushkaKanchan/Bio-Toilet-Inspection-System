from math import floor

from apps.inspection.dto import (
    DefectSummaryDTO,
    InspectionDetailsItemDTO,
    InspectionSummaryDTO,
    MappingStatusDTO,
    TrainInfoDTO,
)
from apps.inspection.models import Inspection, InspectionStatus
from apps.inspection.repositories import InspectionRepository


class InspectionDetailsService:

    def __init__(
        self,
        *,
        repository: InspectionRepository | None = None,
    ) -> None:
        self._repository = repository or InspectionRepository()

    def get_details(
        self,
        *,
        inspection_id,
    ) -> InspectionDetailsItemDTO:

        inspection = self._repository.get_details(
            inspection_id=inspection_id,
        )

        defects = self._repository.get_defect_summary(
            inspection=inspection,
        )

        train = TrainInfoDTO(
            number=inspection.train_number,
            name=inspection.train_name,
            coaches_synchronized=inspection.ntes_total_coaches or 0,
        )

        inspection_summary = InspectionSummaryDTO(
            started_at=inspection.inspection_time,
            duration_minutes=self._duration_minutes(inspection),
            coaches_detected=inspection.total_coaches,
            total_coaches=inspection.ntes_total_coaches or 0,
            total_defects=inspection.total_defected_tanks,
        )
        summary = {
            "PIPE_NOT_CONNECTED": 0,
            "PIPE_SUPPORT_ABSENT": 0,
            "SURFACE_NOT_CLEAN": 0,
        }

        for defect in defects:
            summary[defect["defect_type"]] = defect["count"]

        defect_summary = DefectSummaryDTO(
            pipe_not_connected=summary["PIPE_NOT_CONNECTED"],
            pipe_support_absent=summary["PIPE_SUPPORT_ABSENT"],
            surface_not_clean=summary["SURFACE_NOT_CLEAN"],
        )

        mapping = MappingStatusDTO(
            completed=(inspection.status == InspectionStatus.COMPLETED),
            message=(
                f"Coach composition verified against train "
                f"{inspection.train_number}."
            ),
            train=train,
        )

        return InspectionDetailsItemDTO(
            inspection_id=str(inspection.id),
            status=inspection.status,
            pit_line=inspection.pit_line_number,
            train=train,
            inspection=inspection_summary,
            defect_summary=defect_summary,
            mapping=mapping,
        )

    def _duration_minutes(self, inspection: Inspection) -> int:
        duration = inspection.updated_at - inspection.inspection_time
        minutes = floor(duration.total_seconds() / 60)
        return max(minutes, 0)