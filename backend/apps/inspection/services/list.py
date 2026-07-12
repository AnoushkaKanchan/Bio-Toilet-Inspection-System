from math import floor

from apps.inspection.dto import InspectionListItemDTO
from apps.inspection.models import InspectionStatus
from apps.inspection.repositories import InspectionRepository


class InspectionListService:

    def __init__(
        self,
        *,
        repository: InspectionRepository | None = None,
    ) -> None:
        self._repository = repository or InspectionRepository()

    def list(
        self,
        *,
        status: str | None = None,
    ) -> list[InspectionListItemDTO]:

        if status is not None and status not in InspectionStatus.values:
            raise ValueError("Invalid inspection status.")

        inspections = self._repository.list(
            status=status,
        )

        result = []

        for inspection in inspections:
            result.append(
                InspectionListItemDTO(
                    inspection_id=str(
                        inspection.id,
                    ),
                    train_number=inspection.train_number,
                    pit_line=inspection.pit_line_number,
                    status=inspection.status,
                    inspection_time=inspection.inspection_time,
                    duration_minutes=self._duration_minutes(
                        inspection,
                    ),
                    total_coaches=inspection.total_coaches,
                    total_defects=inspection.total_defected_tanks,
                )
            )

        return result

    def _duration_minutes(
        self,
        inspection,
    ) -> int:
        duration = inspection.updated_at - inspection.inspection_time

        return floor(
            duration.total_seconds() / 60,
        )
