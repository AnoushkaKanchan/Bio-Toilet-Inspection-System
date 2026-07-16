import random

from django.db import transaction

from apps.ai.dto import AIAcknowledgementDTO
from apps.ai.exceptions import DuplicateAIResultError
from apps.ai.services import (
    AIContractValidator,
    AIResultPersistenceService,
)
from apps.inspection.repositories import InspectionRepository
from apps.inspection.models import InspectionStatus
from apps.ai.repositories import AIResultRawRepository


class AIResultService:

    def __init__(
        self,
        validator=None,
        persistence_service=None,
        inspection_repository=None,
        ai_result_repository=None,
    ):
        self._validator = (
            validator
            or AIContractValidator()
        )

        self._persistence_service = (
            persistence_service
            or AIResultPersistenceService()
        )

        self._inspection_repository = (
            inspection_repository
            or InspectionRepository()
        )

        self._ai_result_repository = (
            ai_result_repository
            or AIResultRawRepository()
        )

    @transaction.atomic
    def process(
        self,
        *,
        payload: dict,
    ):
        # 1. Validate AI payload
        self._validator.validate(payload)

        # 2. Check duplicate FIRST, before creating anything
        if self._ai_result_repository.exists(
            inspection_run_id=payload["inspection_run_id"],
        ):
            raise DuplicateAIResultError(
                f"AI result '{payload['inspection_run_id']}' already exists."
            )

        # 3. Resolve pit line and Create Inspection
        pit_line_number = self._resolve_pit_line(
            payload=payload,
        )

        inspection = self._inspection_repository.create(
            pit_line_number=pit_line_number,
            inspection_time=payload["processing_timestamp"],
        )

        # 4. Store raw payload
        self._ai_result_repository.create(
            inspection=inspection,
            inspection_run_id=payload["inspection_run_id"],
            status=payload["status"],
            payload=payload,
        )

        # 5. Normalize tanks
        self._persistence_service.persist_tanks(
            inspection=inspection,
            payload=payload,
        )

        # 6. Refresh inspection summary from live counts
        statistics = self._inspection_repository.get_statistics(
            inspection=inspection,
        )

        self._inspection_repository.update_summary(
            inspection=inspection,
            statistics=statistics,
        )

        # 6. Calculate tank metrics
        total_tanks = len(payload["tanks"])
        total_defected_tanks = sum(
            1
            for tank in payload["tanks"]
            if tank["maintenance_status"] == "Maintenance Required"
        )

        return AIAcknowledgementDTO(
            success=True,
            inspection_id=str(inspection.id),
            message="Inspection created and AI results processed successfully.",
        )

    def _resolve_pit_line(
        self,
        *,
        payload: dict,
    ) -> str:
        """
        Temporary development fallback.

        TODO:
        Replace random pit line generation with AI-provided
        pit_line_number before production.
        """
        return payload.get(
            "pit_line_number",
            f"PL-{random.randint(1, 5):02d}",
        )