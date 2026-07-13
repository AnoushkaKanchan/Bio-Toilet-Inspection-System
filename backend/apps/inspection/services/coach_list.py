from apps.inspection.dto import (
    CoachListItemDTO,
    CoachListResponseDTO,
)
from apps.mapping.enums import (
    CoachFilter,
    CoachStatus,
    CoachSideStatus,
)
from apps.inspection.repositories import InspectionRepository
from apps.mapping.models import CameraSide, Coach
from apps.mapping.enums import (
    CoachFilter,
    CoachStatus,
    CoachSideStatus,
)
from apps.mapping.repositories import CoachRepository


class CoachListService:

    def __init__(
        self,
        *,
        inspection_repository: InspectionRepository | None = None,
        coach_repository: CoachRepository | None = None,
    ) -> None:
        self._inspection_repository = (
            inspection_repository or InspectionRepository()
        )

        self._coach_repository = (
            coach_repository or CoachRepository()
        )

    def get_coaches(
        self,
        *,
        inspection_id,
        search: str | None = None,
        filter_by: str = CoachFilter.ALL,
    ) -> CoachListResponseDTO:
        # 1. Validate filter upfront before executing queries
        if filter_by not in CoachFilter.values:
            raise ValueError("Invalid coach filter.")

        # 2. Fetch required domain models
        inspection = self._inspection_repository.get(
            inspection_id=inspection_id,
        )

        coaches = list(
            self._coach_repository.get_detailed_by_inspection(
                inspection=inspection,
            )
        )

        # 3. Apply optional search constraint
        if search:
            search = search.lower()
            coaches = [
                coach
                for coach in coaches
                if coach.ntes_coach
                and search in coach.ntes_coach.coach_number.lower()
            ]

        # 4. Transform entities to DTO items
        coach_items = [
            self._build_coach_item(coach)
            for coach in coaches
        ]

        # 5. Apply memory-cached data status filtering
        if filter_by == CoachFilter.DEFECT:
            coach_items = [
                coach for coach in coach_items if coach.status == CoachStatus.DEFECT
            ]
        elif filter_by == CoachFilter.CLEAN:
            coach_items = [
                coach for coach in coach_items if coach.status == CoachStatus.CLEAN
            ]

        # 6. Return response layout contract
        return CoachListResponseDTO(
            inspection_id=str(inspection.id),
            train_number=inspection.train_number,
            train_name=inspection.train_name,
            coaches=coach_items,
        )

    def _build_coach_item(
        self,
        coach: Coach,
    ) -> CoachListItemDTO:
        # Precompute target computation values once
        defect_count = self._defect_count(coach)
        status = CoachStatus.DEFECT if defect_count > 0 else CoachStatus.CLEAN

        return CoachListItemDTO(
            coach_id=str(coach.id),
            inspection_sequence=coach.inspection_sequence,
            coach_number=self._coach_number(coach),
            coach_type=self._coach_type(coach),
            status=status,
            left_side=self._left_side(coach),
            right_side=self._right_side(coach),
            confidence=self._confidence(coach),
            tank_count=self._tank_count(coach),
            defect_count=defect_count,
        )

    def _coach_number(
        self,
        coach: Coach,
    ) -> str:
        if coach.ntes_coach:
            return coach.ntes_coach.coach_number
        return "UNMATCHED"

    def _coach_type(
        self,
        coach: Coach,
    ) -> str:
        if coach.ntes_coach:
            return coach.ntes_coach.coach_type
        return "Unknown"

    def _left_side(
        self,
        coach: Coach,
    ) -> CoachSideStatus:
        has_left_defects = any(
            tank.camera == CameraSide.LEFT 
            and bool(tank.defects.all())
            for tank in coach.tanks.all()
        )
        return CoachSideStatus.DEFECT if has_left_defects else CoachSideStatus.NORMAL

    def _right_side(
        self,
        coach: Coach,
    ) -> CoachSideStatus:
        has_right_defects = any(
            tank.camera == CameraSide.RIGHT 
            and bool(tank.defects.all())
            for tank in coach.tanks.all()
        )
        return CoachSideStatus.DEFECT if has_right_defects else CoachSideStatus.NORMAL

    def _confidence(
        self,
        coach: Coach,
    ) -> float:
        tanks = list(coach.tanks.all())
        if not tanks:
            return 0.0

        total = sum(float(tank.confidence) for tank in tanks)
        return round(total / len(tanks), 1)

    def _tank_count(
        self,
        coach: Coach,
    ) -> int:
        return len(coach.tanks.all())

    def _defect_count(
        self,
        coach: Coach,
    ) -> int:
        return sum(
            len(tank.defects.all())
            for tank in coach.tanks.all()
        )