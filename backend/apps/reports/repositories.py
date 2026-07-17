from apps.inspection.models import (
    Inspection,
    InspectionStatus,
)
from apps.mapping.models import Coach, Tank, TankDefect
from apps.reports.dto import (
    AIObservationDTO,
    CommonDefectDTO,
    DailyBreakdownDTO,
    DailyReportDTO,
    MonthlyOverviewDTO,
    MonthlyReportDTO,
    MonthlySummaryDTO,
    PitLinePerformanceDTO,
    TodaySummaryDTO,
    TrainInspectionRowDTO,
    WeekComparisonDTO,
    WeeklyReportDTO,
    WeeklySummaryDTO,
    WeeklyTotalsDTO,
)
import calendar
from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

# ... rest of your existing imports stay the same

# TODO: confirm these match your actual TankDefectType enum values.
# These are placeholders based on the defect names shown in the sample report.
CLEANING_RELATED_DEFECT_TYPES = {
    "surface_not_clean",
}

# TODO: define which defect types count as safety-critical for your system.
# Currently empty, so AI observation always reports zero critical defects.
CRITICAL_DEFECT_TYPES: set[str] = set()


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
            coaches_inspected=Coach.objects.filter(
                inspection__in=inspections,
            ).count(),
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
        inspections=None,
    ) -> list[CommonDefectDTO]:
        queryset = TankDefect.objects.all()

        if inspections is not None:
            queryset = queryset.filter(
                tank__coach__inspection__in=inspections,
            )

        queryset = (
            queryset.values(
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

    def get_daily_report(
        self,
    ) -> DailyReportDTO:
        today = timezone.localdate()

        inspections = Inspection.objects.filter(
            created_at__date=today,
        )

        summary = self.get_today_summary()

        train_rows = [
            TrainInspectionRowDTO(
                train_number=inspection.train_number or "—",
                pit_line_number=inspection.pit_line_number,
                coaches=inspection.total_coaches,
                tanks=inspection.total_tanks,
                defects=inspection.total_defected_tanks,
            )
            for inspection in inspections
        ]

        common_defects = self.get_common_defects(
            limit=3,
            inspections=inspections,
        )

        total_tanks = summary.bio_tanks_inspected
        total_defects = summary.defects_found

        pass_percentage = (
            round(
                ((total_tanks - total_defects) / total_tanks) * 100,
            )
            if total_tanks
            else 0
        )

        critical_defects_found = TankDefect.objects.filter(
            tank__coach__inspection__in=inspections,
            defect_type__in=CRITICAL_DEFECT_TYPES,
        ).count()

        cleaning_required_coaches = (
            Coach.objects.filter(
                inspection__in=inspections,
                tanks__defects__defect_type__in=CLEANING_RELATED_DEFECT_TYPES,
            )
            .distinct()
            .count()
        )

        ai_observation = AIObservationDTO(
            total_tanks_inspected=total_tanks,
            pass_percentage=pass_percentage,
            critical_defects_found=critical_defects_found,
            cleaning_required_coaches=cleaning_required_coaches,
        )

        return DailyReportDTO(
            report_date=today,
            generated_at=timezone.now(),
            summary=summary,
            train_rows=train_rows,
            common_defects=common_defects,
            ai_observation=ai_observation,
        )
    
    def get_weekly_report(
        self,
    ) -> WeeklyReportDTO:
        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        week_inspections = Inspection.objects.filter(
            created_at__date__gte=week_start,
            created_at__date__lte=week_end,
        )

        daily_breakdown: list[DailyBreakdownDTO] = []

        for offset in range(7):
            day = week_start + timedelta(days=offset)

            day_inspections = Inspection.objects.filter(
                created_at__date=day,
            )

            day_defects = TankDefect.objects.filter(
                tank__coach__inspection__in=day_inspections,
            ).count()

            daily_breakdown.append(
                DailyBreakdownDTO(
                    day_label=day.strftime("%A"),
                    trains=day_inspections.count(),
                    defects=day_defects,
                )
            )

        total_trains = sum(row.trains for row in daily_breakdown)
        total_defects = sum(row.defects for row in daily_breakdown)

        total_coaches = Coach.objects.filter(
            inspection__in=week_inspections,
        ).count()

        total_tanks = Tank.objects.filter(
            coach__inspection__in=week_inspections,
        ).count()

        average_defects_per_train = (
            round(total_defects / total_trains, 2) if total_trains else 0.0
        )

        top_defects = self.get_common_defects(
            limit=3,
            inspections=week_inspections,
        )

        # TODO: this is a simple heuristic, not a real model/AI call.
        # Replace with actual analysis logic once available.
        ai_analysis: list[str] = []

        if daily_breakdown:
            busiest_day = max(daily_breakdown, key=lambda row: row.trains)
            worst_defect_day = max(daily_breakdown, key=lambda row: row.defects)

            ai_analysis.append(
                f"{busiest_day.day_label} had the highest train volume "
                f"({busiest_day.trains} trains)."
            )
            ai_analysis.append(
                f"{worst_defect_day.day_label} recorded the most defects "
                f"({worst_defect_day.defects})."
            )

        if average_defects_per_train:
            ai_analysis.append(
                f"Average of {average_defects_per_train} defects per train "
                f"this week."
            )

        return WeeklyReportDTO(
            week_start=week_start,
            week_end=week_end,
            generated_at=timezone.now(),
            daily_breakdown=daily_breakdown,
            totals=WeeklyTotalsDTO(
                total_trains=total_trains,
                total_coaches=total_coaches,
                total_tanks=total_tanks,
                average_defects_per_train=average_defects_per_train,
            ),
            top_defects=top_defects,
            ai_analysis=ai_analysis,
        )

    def get_monthly_report(
        self,
    ) -> MonthlyReportDTO:
        today = timezone.localdate()
        month_start = today.replace(day=1)
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        month_end = today.replace(day=days_in_month)

        month_inspections = Inspection.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end,
        )

        trains_inspected = month_inspections.count()

        coaches_inspected = Coach.objects.filter(
            inspection__in=month_inspections,
        ).count()

        bio_tanks_inspected = Tank.objects.filter(
            coach__inspection__in=month_inspections,
        ).count()

        completed = month_inspections.filter(
            status=InspectionStatus.COMPLETED,
        ).count()

        total_defects = TankDefect.objects.filter(
            tank__coach__inspection__in=month_inspections,
        ).count()

        average_defects_per_train = (
            round(total_defects / trains_inspected, 2)
            if trains_inspected
            else 0.0
        )

        overview = MonthlyOverviewDTO(
            trains_inspected=trains_inspected,
            coaches_inspected=coaches_inspected,
            bio_tanks_inspected=bio_tanks_inspected,
            completed=completed,
            average_defects_per_train=average_defects_per_train,
        )

        # TODO: buckets days [1-7], [8-14], [15-21], [22-end] into 4 fixed
        # "weeks" for simplicity. This does not follow ISO week numbering
        # and the last bucket may span more or fewer than 7 days depending
        # on the month length. Adjust if you need calendar-accurate weeks.
        week_ranges = [
            (1, 7),
            (8, 14),
            (15, 21),
            (22, days_in_month),
        ]

        weekly_comparison: list[WeekComparisonDTO] = []

        for index, (start_day, end_day) in enumerate(week_ranges, start=1):
            range_start = today.replace(day=start_day)
            range_end = today.replace(day=end_day)

            range_inspections = Inspection.objects.filter(
                created_at__date__gte=range_start,
                created_at__date__lte=range_end,
            )

            range_defects = TankDefect.objects.filter(
                tank__coach__inspection__in=range_inspections,
            ).count()

            weekly_comparison.append(
                WeekComparisonDTO(
                    week_label=f"Week {index}",
                    trains=range_inspections.count(),
                    defects=range_defects,
                )
            )

        most_frequent_defects = self.get_common_defects(
            limit=5,
            inspections=month_inspections,
        )

        # TODO: "performance" here is inspections + defects + defect rate
        # per pit line. Adjust the metric if you have a different
        # definition of pit line "performance" in mind.
        pit_line_numbers = (
            month_inspections.values_list(
                "pit_line_number",
                flat=True,
            )
            .distinct()
            .order_by("pit_line_number")
        )

        pit_line_performance: list[PitLinePerformanceDTO] = []

        for pit_line_number in pit_line_numbers:
            pit_inspections = month_inspections.filter(
                pit_line_number=pit_line_number,
            )

            pit_defects = TankDefect.objects.filter(
                tank__coach__inspection__in=pit_inspections,
            ).count()

            inspections_count = pit_inspections.count()

            pit_line_performance.append(
                PitLinePerformanceDTO(
                    pit_line_number=pit_line_number,
                    inspections=inspections_count,
                    defects=pit_defects,
                    average_defects_per_inspection=(
                        round(pit_defects / inspections_count, 2)
                        if inspections_count
                        else 0.0
                    ),
                )
            )

        # TODO: simple heuristic, not a real model/AI call.
        ai_recommendations: list[str] = []

        if most_frequent_defects:
            top_defect = most_frequent_defects[0]
            ai_recommendations.append(
                f"'{top_defect.display_name}' is the most common defect this "
                f"month ({top_defect.count} occurrences) — consider a "
                f"targeted maintenance pass."
            )

        if pit_line_performance:
            worst_pit = max(
                pit_line_performance,
                key=lambda row: row.average_defects_per_inspection,
            )
            if worst_pit.average_defects_per_inspection > 0:
                ai_recommendations.append(
                    f"Pit line {worst_pit.pit_line_number} has the highest "
                    f"average defect rate "
                    f"({worst_pit.average_defects_per_inspection} per "
                    f"inspection) — flag for review."
                )

        return MonthlyReportDTO(
            month_label=today.strftime("%B %Y"),
            generated_at=timezone.now(),
            overview=overview,
            weekly_comparison=weekly_comparison,
            most_frequent_defects=most_frequent_defects,
            pit_line_performance=pit_line_performance,
            ai_recommendations=ai_recommendations,
        )