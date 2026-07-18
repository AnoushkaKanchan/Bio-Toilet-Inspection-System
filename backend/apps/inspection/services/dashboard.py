from math import floor

from django.db.models.aggregates import Count
from django.utils import timezone

from apps.inspection.repositories import InspectionRepository
from apps.mapping.repositories import CoachRepository
from apps.reports.services.dashboard import DashboardService as ReportsDashboardService
from apps.mapping.models import TankDefect
from apps.mapping.enums import TankDefectType


class DashboardService:

    def __init__(
        self,
        reports_dashboard_service: ReportsDashboardService | None = None,
        repository: InspectionRepository | None = None,
        coach_repository: CoachRepository | None = None,
    ) -> None:
        self._reports_dashboard_service = (
            reports_dashboard_service or ReportsDashboardService()
        )
        self._repository = repository or InspectionRepository()
        self._coach_repository = coach_repository or CoachRepository()

    def get_summary(self) -> dict:
        dashboard = self._reports_dashboard_service.get_dashboard_summary()

        return {
            "today": {
                "trains_inspected": dashboard.today.trains_inspected,
                "bio_tanks_inspected": dashboard.today.bio_tanks_inspected,
                "defects_found": dashboard.today.defects_found,
                "completed_inspections": dashboard.today.completed,
            }
        }

    def get_live_pitlines(self) -> dict:
        inspections = self._repository.get_todays_inspections()

        result = []

        for inspection in inspections:
            result.append(
                {
                    "inspection_id": str(inspection.id),
                    "pit_line": inspection.pit_line_number,
                    "train_number": inspection.train_number,
                    "status": inspection.status,
                    "started_at": inspection.created_at.isoformat(),
                    "duration_minutes": self._get_duration_minutes(inspection=inspection),
                    "defects": inspection.total_defected_tanks,
                    "inspected_coaches": inspection.total_coaches,
                    "total_coaches": inspection.ntes_total_coaches or 0,
                    "defect_summary": self._get_defect_summary(inspection=inspection),
                }
            )

        return {"pit_lines": result}

    def get_operations_status(self) -> dict:
        inspections = self._repository.get_active_inspections()

        if not inspections:
            return {
                "status": "IDLE",
                "message": "No inspection is currently running.",
            }

        inspection = inspections[0]

        return {
            "status": inspection.status,
            "message": (
                f"Pit Line {inspection.pit_line_number} "
                f"inspecting Train {inspection.train_number}."
            ),
        }

    def get_recent_activity(self) -> dict:
        inspections = self._repository.get_recent_inspections()

        activities = []

        for inspection in inspections:
            activities.append(
                {
                    "inspection_id": str(inspection.id),
                    "train_number": inspection.train_number,
                    "pit_line": inspection.pit_line_number,
                    "status": inspection.status,
                    "timestamp": inspection.created_at.isoformat(),
                }
            )

        return {
            "activities": activities,
        }

    def get_train_mapping(
        self,
        *,
        inspection_id,
    ) -> dict:
        inspection = self._repository.get(
            inspection_id=inspection_id,
        )

        coaches = self._coach_repository.get_by_inspection(
            inspection=inspection,
        )

        result = []

        for coach in coaches:
            result.append(
                {
                    "coach_number": (
                        coach.ntes_coach.coach_number if coach.ntes_coach else None
                    ),
                    "coach_type": (
                        coach.ntes_coach.coach_type if coach.ntes_coach else None
                    ),
                    "mapping_status": coach.mapping_status,
                    "inspection_status": coach.coach_inspection_status,
                }
            )

        return {
            "inspection_id": str(inspection.id),
            "train_number": inspection.train_number,
            "coaches": result,
        }

    def _get_defect_summary(self, *, inspection) -> dict:
        counts = (
            TankDefect.objects.filter(
                tank__coach__inspection=inspection,
            )
            .values("defect_type")
            .annotate(count=Count("id"))
        )

        by_type = {row["defect_type"]: row["count"] for row in counts}

        return {
            "pipe_not_connected": by_type.get(TankDefectType.PIPE_NOT_CONNECTED, 0),
            "pipe_support_absent": by_type.get(TankDefectType.PIPE_SUPPORT_ABSENT, 0),
            "surface_not_clean": by_type.get(TankDefectType.SURFACE_NOT_CLEAN, 0),
        }

    def _get_duration_minutes(self, *, inspection) -> int:
        now = timezone.now()
        duration = now - inspection.created_at
        minutes = floor(duration.total_seconds() / 60)
        return max(minutes, 0)