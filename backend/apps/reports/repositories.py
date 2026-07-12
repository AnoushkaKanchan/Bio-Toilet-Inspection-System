from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from apps.inspection.models import (
    Inspection,
    InspectionStatus,
)
from apps.mapping.models import Coach, Tank, TankDefect
from apps.reports.dto import (
    CommonDefectDTO,
    MonthlySummaryDTO,
    TodaySummaryDTO,
    WeeklySummaryDTO,
)


class ReportsRepository:
    def get_today_summary(
        self,
    ) -> TodaySummaryDTO:
        today = timezone.localdate()

        inspections = Inspection.objects.filter(
            created_at__date=today,
        )

        return TodaySummaryDTO(
            trains_inspected=inspections.count(),
            bio_tanks_inspected=Tank.objects.filter(
                coach__inspection__in=inspections,
            ).count(),
            defects_found=TankDefect.objects.filter(
                tank__coach__inspection__in=inspections,
            ).count(),
            completed=inspections.filter(
                status=InspectionStatus.COMPLETED,
            ).count(),
        )

    def get_weekly_summary(
        self,
    ) -> WeeklySummaryDTO:
        start = timezone.now() - timedelta(days=7)

        inspections = Inspection.objects.filter(
            created_at__gte=start,
        )

        return WeeklySummaryDTO(
            trains_inspected=inspections.count(),
            coaches_inspected=Coach.objects.filter(
                inspection__in=inspections,
            ).count(),
            bio_tanks_inspected=Tank.objects.filter(
                coach__inspection__in=inspections,
            ).count(),
            total_defects=TankDefect.objects.filter(
                tank__coach__inspection__in=inspections,
            ).count(),
        )

    def get_monthly_summary(
        self,
    ) -> MonthlySummaryDTO:
        start = timezone.now() - timedelta(days=30)

        inspections = Inspection.objects.filter(
            created_at__gte=start,
        )

        return MonthlySummaryDTO(
            trains_inspected=inspections.count(),
            coaches_inspected=Coach.objects.filter(
                inspection__in=inspections,
            ).count(),
            bio_tanks_inspected=Tank.objects.filter(
                coach__inspection__in=inspections,
            ).count(),
            total_defects=TankDefect.objects.filter(
                tank__coach__inspection__in=inspections,
            ).count(),
        )

    def get_common_defects(
        self,
        *,
        limit: int = 10,
    ) -> list[CommonDefectDTO]:
        queryset = (
            TankDefect.objects.values(
                "defect_type",
            )
            .annotate(
                count=Count("id"),
            )
            .order_by("-count")[:limit]
        )

        return [
            CommonDefectDTO(
                defect_type=row["defect_type"],
                display_name=row["defect_type"]
                .replace(
                    "_",
                    " ",
                )
                .title(),
                count=row["count"],
            )
            for row in queryset
        ]
