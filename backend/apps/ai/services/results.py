from apps.ai.dto import AIAcknowledgementDTO
from apps.ai.services import (
    AIContractValidator,
    AIResultPersistenceService,
)
from apps.inspection.repositories import InspectionRepository
from apps.mapping.services.orchestrator import MappingOrchestrator
from apps.mapping.services.persistence import RailwayMappingPersistence


class AIResultService:

    def __init__(
        self,
        *,
        validator: AIContractValidator | None = None,
        persistence_service: AIResultPersistenceService | None = None,
        inspection_repository: InspectionRepository | None = None,
        mapping_orchestrator: MappingOrchestrator | None = None,
        mapping_persistence: RailwayMappingPersistence | None = None,
    ) -> None:

        self._validator = (
            validator or AIContractValidator()
        )

        self._persistence_service = (
            persistence_service
            or AIResultPersistenceService()
        )

        self._inspection_repository = (
            inspection_repository
            or InspectionRepository()
        )

        self._mapping_orchestrator = (
            mapping_orchestrator
            or MappingOrchestrator()
        )

        self._mapping_persistence = (
            mapping_persistence
            or RailwayMappingPersistence()
        )

    def process(
        self,
        *,
        inspection_id,
        payload: dict,
    ) -> AIAcknowledgementDTO:

        # Validate incoming payload
        self._validator.validate(
            payload=payload,
        )

        # Load inspection
        inspection = self._inspection_repository.get(
            inspection_id=inspection_id,
        )

        # Persist immutable payload
        self._persistence_service.persist(
            inspection=inspection,
            payload=payload,
        )

        # Resolve AI coaches to NTES coaches
        resolved_coaches = (
            self._mapping_orchestrator.execute(
                payload=payload,
                coaches=list(
                    inspection.ntes_coaches.all(),
                ),
            )
        )

        # Persist mapping entities
        for resolved in resolved_coaches:

            coach = (
                self._mapping_persistence.create_coach(
                    inspection=inspection,
                    resolved_coach=resolved,
                )
            )

            for tank_payload in resolved.tanks:

                tank = (
                    self._mapping_persistence.create_tank(
                        coach=coach,
                        tank_data=tank_payload,
                    )
                )

                defects = (
                    self._mapping_orchestrator.mapper.translate_defects(
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

        return AIAcknowledgementDTO(
            success=True,
            inspection_id=str(
                inspection.id,
            ),
            message="AI results processed successfully.",
        )