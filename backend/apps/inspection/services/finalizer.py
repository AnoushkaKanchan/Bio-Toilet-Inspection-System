from apps.inspection.dto import InspectionStatistics
from apps.inspection.exceptions import (
    InspectionFinalizationError,
)
from apps.inspection.models import Inspection
from apps.mapping.models import Coach, Tank

_INSPECTION_SUMMARY_FIELDS = (
    "total_coaches",
    "total_tanks",
    "total_defected_tanks",
)


class InspectionFinalizer:
    def finalize(
        self,
        *,
        inspection: Inspection,
    ) -> Inspection:
        statistics = self._compute_statistics(
            inspection,
        )

        self._verify_statistics(
            statistics,
        )

        self._update_inspection(
            inspection,
            statistics,
        )

        return inspection

    def _compute_statistics(
        self,
        inspection: Inspection,
    ) -> InspectionStatistics:
        total_coaches = Coach.objects.filter(
            inspection=inspection,
        ).count()

        total_tanks = Tank.objects.filter(
            coach__inspection=inspection,
        ).count()

        total_defected_tanks = (
            Tank.objects.filter(
                coach__inspection=inspection,
                defects__isnull=False,
            )
            .distinct()
            .count()
        )

        return InspectionStatistics(
            total_coaches=total_coaches,
            total_tanks=total_tanks,
            total_defected_tanks=total_defected_tanks,
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

    def _update_inspection(
        self,
        inspection: Inspection,
        statistics: InspectionStatistics,
    ) -> None:
        inspection.total_coaches = statistics.total_coaches

        inspection.total_tanks = statistics.total_tanks

        inspection.total_defected_tanks = statistics.total_defected_tanks

        inspection.save(
            update_fields=_INSPECTION_SUMMARY_FIELDS,
        )
