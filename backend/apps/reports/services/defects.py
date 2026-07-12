from apps.reports.dto import CommonDefectDTO
from apps.reports.repositories import ReportsRepository


class CommonDefectsService:
    def __init__(
        self,
        *,
        repository: ReportsRepository | None = None,
    ) -> None:
        self._repository = repository or ReportsRepository()

    def get_common_defects(
        self,
        *,
        limit: int = 10,
    ) -> list[CommonDefectDTO]:
        return self._repository.get_common_defects(
            limit=limit,
        )
