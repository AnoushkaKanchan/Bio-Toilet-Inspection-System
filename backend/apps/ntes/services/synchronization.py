import logging
import time

from django.db import transaction

from apps.ai.repositories import AIResultRawRepository
from apps.inspection.models import Inspection
from apps.mapping.services.workflow import MappingWorkflowService
from apps.ntes.clients import PlaywrightNTESClient
from apps.ntes.models import NTESCoach
from apps.ntes.normalizer import NTESNormalizer
from apps.ntes.parser import NTESHTMLParser
from apps.ntes.repositories import NTESCoachRepository
from apps.ntes.services.verification import NTESVerificationService

logger = logging.getLogger(__name__)


class SynchronizationService:
    def __init__(
        self,
        *,
        client: PlaywrightNTESClient | None = None,
        parser: NTESHTMLParser | None = None,
        normalizer: NTESNormalizer | None = None,
        repository: NTESCoachRepository | None = None,
        verifier: NTESVerificationService | None = None,
        ai_repository: AIResultRawRepository | None = None,
        mapping_workflow: MappingWorkflowService | None = None,
    ) -> None:
        self._client = client or PlaywrightNTESClient()
        self._parser = parser or NTESHTMLParser()
        self._normalizer = normalizer or NTESNormalizer()
        self._repository = repository or NTESCoachRepository()
        self._verifier = verifier or NTESVerificationService(
            repository=self._repository,
        )
        self._ai_repository = ai_repository or AIResultRawRepository()
        self._mapping_workflow = mapping_workflow or MappingWorkflowService()

    @transaction.atomic
    def synchronize(
        self,
        *,
        inspection: Inspection,
    ) -> list[NTESCoach]:
        start = time.monotonic()

        logger.info(
            "Starting NTES synchronization for inspection %s (train %s).",
            inspection.id,
            inspection.train_number,
        )

        html_result = self._client.fetch(
            train_number=inspection.train_number,
        )

        inspection.train_name = html_result["train_name"]
        inspection.save(
            update_fields=["train_name"],
        )

        raw_coaches = self._parser.parse(
            html=html_result["html"],
        )

        coach_dtos = self._normalizer.normalize(
            coaches=raw_coaches,
        )

        self._repository.replace_composition(
            inspection=inspection,
            coaches=coach_dtos,
        )

        # apps/ntes/services/synchronization.py
        coaches = self._verifier.verify(
            inspection=inspection,
        )

        inspection.ntes_total_coaches = len(coaches)
        inspection.save(update_fields=["ntes_total_coaches"])

        # Check if an AI payload is already present for mapping
        ai_result = self._ai_repository.get_latest_by_inspection(
            inspection=inspection,
        )

        if ai_result :
            logger.info("AI result detected. Delegating mapping workflow execution.")
            
            self._mapping_workflow.execute(
                inspection=inspection,
                payload=ai_result.payload,
                coaches=coaches,
            )
        else:
            logger.info(
                "No AI result available. Mapping workflow skipped.",
            )

        logger.info(
            "Completed NTES synchronization for inspection %s in %.2f seconds.",
            inspection.id,
            time.monotonic() - start,
        )

        return coaches