from apps.inspection.repositories import InspectionRepository
from apps.mapping.repositories import CoachRepository
from apps.reports.services.dashboard import DashboardService as ReportsDashboardService
from apps.mapping.models import MappingStatus


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
                    "pit_line": inspection.pit_line_number,
                    "train_number": inspection.train_number,
                    "status": inspection.status,
                    "started_at": inspection.created_at.isoformat(),
                    "defects": inspection.total_defected_tanks,
                    "inspected_coaches": inspection.total_coaches,
                    "total_coaches": inspection.ntes_total_coaches or 0,
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
