from apps.ai.dto import AIAcknowledgementDTO
from apps.ai.services import (
    AIContractValidator,
    AIResultPersistenceService,
)
from apps.inspection.repositories import InspectionRepository


class AIResultService:

    def __init__(
        self,
        *,
        validator: AIContractValidator | None = None,
        persistence_service: AIResultPersistenceService | None = None,
        inspection_repository: InspectionRepository | None = None,
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

        return AIAcknowledgementDTO(
            success=True,
            inspection_id=str(
                inspection.id,
            ),
            message="AI results processed successfully.",
        )