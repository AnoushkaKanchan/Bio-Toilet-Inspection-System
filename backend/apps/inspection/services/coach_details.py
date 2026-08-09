from apps.inspection.dto import (
    CoachInfoDTO,
    CoachInspectionImageDTO,
    CoachInspectionImagesDTO,
    CoachInspectionReportDTO,
    CoachInspectionSummaryDTO,
    FindingDTO,
    HealthDiagramDTO,
    NavigationDTO,
)
from apps.inspection.repositories import InspectionRepository
from apps.mapping.enums import (
    CoachSideStatus,
    CoachStatus,
    TankDefectType,
)
from apps.mapping.models import CameraSide
from apps.mapping.repositories import CoachRepository
from statistics import mean

class CoachInspectionReportService:

    def __init__(
        self,
        *,
        inspection_repository: InspectionRepository | None = None,
        coach_repository: CoachRepository | None = None,
    ) -> None:
        self._inspection_repository = (
            inspection_repository
            or InspectionRepository()
        )

        self._coach_repository = (
            coach_repository
            or CoachRepository()
        )

    def get_report(
        self,
        *,
        inspection_id,
        coach_id,
    ) -> CoachInspectionReportDTO:

        inspection = self._inspection_repository.get(
            inspection_id=inspection_id,
        )

        coach = self._coach_repository.get_details(
            inspection=inspection,
            coach_id=coach_id,
        )

        previous = self._coach_repository.get_previous_coach(
            inspection=inspection,
            coach=coach,
        )

        next_coach = self._coach_repository.get_next_coach(
            inspection=inspection,
            coach=coach,
        )

        findings = self._build_findings(
            coach,
        )

        return CoachInspectionReportDTO(
            coach=self._coach_info(
                coach,
            ),
            inspection=self._inspection_summary(
                coach,
            ),
            health_diagram=self._health_diagram(
                coach,
            ),
            findings=findings,
            maintenance=self._maintenance(
                findings,
            ),
            remarks=self._remarks(
                findings,
            ),
            navigation=NavigationDTO(
                previous=str(previous.id)
                if previous
                else None,
                next=str(next_coach.id)
                if next_coach
                else None,
            ),
        )

    def _coach_info(
        self,
        coach,
    ) -> CoachInfoDTO:

        return CoachInfoDTO(
            number=coach.ntes_coach.coach_number,
            type=coach.ntes_coach.coach_type,
            status=(
                CoachStatus.DEFECT
                if any(
                    tank.defects.all()
                    for tank in coach.tanks.all()
                )
                else CoachStatus.CLEAN
            ),
        )

    def _inspection_summary(
        self,
        coach,
    ) -> CoachInspectionSummaryDTO:

        tanks = list(
            coach.tanks.all(),
        )

        confidence = (
            round(
                mean(
                    float(t.confidence)
                    for t in tanks
                )
            )
            if tanks
            else 0
        )

        return CoachInspectionSummaryDTO(
            left_status=self._side_status(
                coach,
                CameraSide.LEFT,
            ),
            right_status=self._side_status(
                coach,
                CameraSide.RIGHT,
            ),
            overall_confidence=confidence,
        )

    def _side_status(
        self,
        coach,
        side,
    ):

        for tank in coach.tanks.all():

            if (
                tank.camera == side
                and tank.defects.all()
            ):
                return CoachSideStatus.DEFECT

        return CoachSideStatus.NORMAL

    def _health_diagram(
        self,
        coach,
    ) -> HealthDiagramDTO:

        left = self._side_status(
            coach,
            CameraSide.LEFT,
        )

        right = self._side_status(
            coach,
            CameraSide.RIGHT,
        )

        return HealthDiagramDTO(
            front_left=left,
            front_right=right,
            rear_left=left,
            rear_right=right,
            bio_tank=CoachSideStatus.NORMAL,
        )

    def _build_findings(
        self,
        coach,
    ):

        findings = []

        for tank in coach.tanks.all():

            for defect in tank.defects.all():

                findings.append(
                    FindingDTO(
                        title=tank.tank_identifier,
                        description=defect.defect_type.replace(
                            "_",
                            " ",
                        ).title(),
                        confidence=int(
                            defect.confidence,
                        ),
                    )
                )

        return findings

    def _maintenance(
        self,
        findings,
    ):

        recommendations = []

        for finding in findings:

            if "PIPE NOT CONNECTED" in finding.description.upper():
                recommendations.append(
                    "Reconnect pipe before next service cycle."
                )

            elif "PIPE SUPPORT ABSENT" in finding.description.upper():
                recommendations.append(
                    "Install pipe support bracket."
                )

            elif "SURFACE NOT CLEAN" in finding.description.upper():
                recommendations.append(
                    "Clean bio tank surface."
                )

        return list(
            dict.fromkeys(
                recommendations,
            )
        )

    def _remarks(
        self,
        findings,
    ):

        if not findings:
            return "No issues detected."

        if len(findings) == 1:
            return (
                "Minor issues detected."
            )

        return (
            "Multiple maintenance issues detected."
        )

    def get_images(
        self,
        *,
        inspection_id,
        coach_id,
    ) -> CoachInspectionImagesDTO:

        inspection = self._inspection_repository.get(
            inspection_id=inspection_id,
        )

        coach = self._coach_repository.get_details(
            inspection=inspection,
            coach_id=coach_id,
        )

        tanks = sorted(
            coach.tanks.all(),
            key=lambda t: t.tank_identifier,
        )

        images = [
            CoachInspectionImageDTO(
                label=f"Image {index}",
                image_url=tank.evidence_image_path,
                tank_identifier=tank.tank_identifier,
                camera_side=tank.camera,
            )
            for index, tank in enumerate(tanks, start=1)
            if tank.evidence_image_path
        ]

        return CoachInspectionImagesDTO(
            coach_type=coach.ntes_coach.coach_type,
            train_number=inspection.train_number,
            images=images,
        )