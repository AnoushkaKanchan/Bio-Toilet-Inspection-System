import logging

from django.db import transaction

from apps.inspection.models import Inspection
from apps.inspection.repositories import InspectionRepository
from apps.mapping.services.orchestrator import MappingOrchestrator
from apps.mapping.services.persistence import RailwayMappingPersistence
from apps.ntes.models import NTESCoach

logger = logging.getLogger(__name__)


class MappingWorkflowService:
    def __init__(
        self,
        *,
        mapping_orchestrator: MappingOrchestrator | None = None,
        mapping_persistence: RailwayMappingPersistence | None = None,
        inspection_repository: InspectionRepository | None = None,
    ) -> None:
        self._mapping_orchestrator = (
            mapping_orchestrator or MappingOrchestrator()
        )

        self._mapping_persistence = (
            mapping_persistence or RailwayMappingPersistence()
        )

        self._inspection_repository = (
            inspection_repository or InspectionRepository()
        )

    @transaction.atomic
    def execute(
        self,
        *,
        inspection: Inspection,
        payload: dict,
        coaches: list[NTESCoach],
    ) -> None:
        """
        Execute the complete railway mapping workflow.

        Responsibilities:
        - Resolve AI tank positions against NTES coach composition.
        - Persist coaches, tanks, and defects.
        - Refresh inspection summary statistics.

        The workflow is idempotent. Any previously generated mapping for the
        inspection is removed before rebuilding the latest structure.
        """

        logger.info(
            "Executing mapping workflow for inspection %s.",
            inspection.id,
        )

        # Ensure repeated executions rebuild the mapping cleanly.
        self._mapping_persistence.clear_mapping(
            inspection=inspection,
        )

        resolved_coaches = (
            self._mapping_orchestrator.execute(
                payload=payload,
                coaches=coaches,
            )
        )

        logger.info(
            "Resolved %d mapped coach(es).",
            len(resolved_coaches),
        )

        for resolved_coach in resolved_coaches:
            coach = (
                self._mapping_persistence.create_coach(
                    inspection=inspection,
                    resolved_coach=resolved_coach,
                )
            )

            for tank_payload in resolved_coach.tanks:
                tank = (
                    self._mapping_persistence.create_tank(
                        coach=coach,
                        tank_data=tank_payload,
                    )
                )

                defects = (
                    self._mapping_orchestrator.translate_defects(
                        tank_payload,
                    )
                )

                self._mapping_persistence.create_tank_defects(
                    tank=tank,
                    defects=defects,
                    confidence=tank_payload[
                        "detection_confidence"
                    ],
                )

        statistics = (
            self._inspection_repository.get_statistics(
                inspection=inspection,
            )
        )

        self._inspection_repository.update_summary(
            inspection=inspection,
            statistics=statistics,
        )

        logger.info(
            "Mapping workflow completed successfully for inspection %s.",
            inspection.id,
        )