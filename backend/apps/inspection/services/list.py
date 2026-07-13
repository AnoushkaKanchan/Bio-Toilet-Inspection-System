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
        search: str | None = None,
    ) -> list[InspectionListItemDTO]:

        if status is not None and status not in InspectionStatus.values:
            raise ValueError("Invalid inspection status.")

        inspections = self._repository.list(
            status=status,
            search=search,
        )

        result = []

        for inspection in inspections:
            result.append(
                InspectionListItemDTO(
                    inspection_id=str(
                        inspection.id,
                    ),
                    train_number=inspection.train_number,
                    # Temporary until train_name is available
                    train_name=inspection.train_name,
                    inspection_time=inspection.inspection_time,
                    pit_line=inspection.pit_line_number,
                    status=inspection.status,
                    issue_count=inspection.total_defected_tanks,
                )
            )

        return result
