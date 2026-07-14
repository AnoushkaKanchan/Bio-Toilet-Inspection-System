from uuid import UUID

from django.db.models import QuerySet
from django.db.models.aggregates import Count

from apps.inspection.dto import InspectionStatistics
from apps.inspection.models import Inspection, InspectionStatus
from apps.mapping.models import Coach, Tank, TankDefect


class InspectionRepository:

    def get(
        self,
        *,
        inspection_id: UUID,
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

    def get_active_inspections(
        self,
    ) -> list[Inspection]:
        return list(
            Inspection.objects.filter(
                status=InspectionStatus.PROCESSING,
            ).order_by(
                "created_at",
            )
        )

    def get_recent_inspections(
        self,
        *,
        limit: int = 10,
    ) -> list[Inspection]:
        return list(
            Inspection.objects.order_by(
                "-created_at",
            )[:limit]
        )

    def list(
        self,
        *,
        status: InspectionStatus | None = None,
        search: str | None = None,
    ) -> QuerySet:

        queryset = Inspection.objects.order_by(
            "-inspection_time",
        )

        if status:
            queryset = queryset.filter(
                status=status,
            )

        if search:
            queryset = queryset.filter(
                train_number__icontains=search,
            )

        return queryset

    def get_details(
        self,
        *,
        inspection_id: UUID,
    ) -> Inspection:
        return self.get(
            inspection_id=inspection_id,
        )

    def get_defect_summary(
        self,
        *,
        inspection: Inspection,
    ) -> QuerySet:
        return (
            TankDefect.objects.filter(
                tank__coach__inspection=inspection,
            )
            .values(
                "defect_type",
            )
            .annotate(
                count=Count("id"),
            )
            .order_by()
        )
