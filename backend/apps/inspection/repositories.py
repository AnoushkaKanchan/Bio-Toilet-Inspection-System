from apps.inspection.dto import InspectionStatistics
from apps.inspection.models import Inspection
from apps.mapping.models import Coach, Tank


class InspectionRepository:
    def get(
        self,
        *,
        inspection_id,
    ) -> Inspection:
        return Inspection.objects.get(
            id=inspection_id,
        )

    def save(
        self,
        *,
        inspection: Inspection,
    ) -> Inspection:
        inspection.save()

        return inspection

    def get_statistics(
        self,
        *,
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

    def update_summary(
        self,
        *,
        inspection: Inspection,
        statistics: InspectionStatistics,
    ) -> Inspection:
        inspection.total_coaches = statistics.total_coaches
        inspection.total_tanks = statistics.total_tanks
        inspection.total_defected_tanks = statistics.total_defected_tanks

        inspection.save(
            update_fields=(
                "total_coaches",
                "total_tanks",
                "total_defected_tanks",
            ),
        )

        return inspection
