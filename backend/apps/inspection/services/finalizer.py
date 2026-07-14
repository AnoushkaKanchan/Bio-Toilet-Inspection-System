from apps.inspection.dto import InspectionStatistics
from apps.inspection.exceptions import InspectionFinalizationError
from apps.inspection.models import Inspection
from apps.inspection.repositories import InspectionRepository


class InspectionFinalizer:
    def __init__(
        self,
        repository: InspectionRepository | None = None,
    ) -> None:
        self._repository = repository or InspectionRepository()

    def finalize(
        self,
        *,
        inspection: Inspection,
    ) -> Inspection:
        statistics = self._repository.get_statistics(
            inspection=inspection,
        )

        self._verify_statistics(
            statistics,
        )

        return self._repository.update_summary(
            inspection=inspection,
            statistics=statistics,
        )

    def _verify_statistics(
        self,
        statistics: InspectionStatistics,
    ) -> None:
        if (
            statistics.healthy_tanks + statistics.total_defected_tanks
            != statistics.total_tanks
        ):
            raise InspectionFinalizationError("Inspection statistics are inconsistent.")
