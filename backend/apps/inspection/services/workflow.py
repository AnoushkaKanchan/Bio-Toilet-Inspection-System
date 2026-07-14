import logging

from apps.inspection.models import Inspection
from apps.inspection.repositories import InspectionRepository
from apps.ntes.models import NTESCoach
from apps.ntes.services import SynchronizationService

logger = logging.getLogger(__name__)


class InspectionWorkflowService:
    def __init__(
        self,
        *,
        repository: InspectionRepository | None = None,
        synchronization_service: SynchronizationService | None = None,
    ) -> None:
        self._repository = repository or InspectionRepository()
        self._synchronization_service = (
            synchronization_service or SynchronizationService()
        )

    def start(
        self,
        *,
        inspection: Inspection,
    ) -> list[NTESCoach]:
        logger.info(
            "Starting inspection workflow for inspection %s.",
            inspection.id,
        )

        coaches = self._synchronization_service.synchronize(
            inspection=inspection,
        )

        logger.info(
            "NTES synchronization completed for inspection %s.",
            inspection.id,
        )

        return coaches
