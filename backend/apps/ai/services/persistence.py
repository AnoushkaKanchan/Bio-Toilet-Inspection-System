from django.db import transaction

from apps.ai.models import AIResultRaw
from apps.ai.repositories import AIResultRawRepository
from apps.inspection.models import Inspection


class AIResultPersistenceService:
    """
    Application service responsible for persisting validated AI payloads.

    Responsibilities:
        - Persist immutable AIResultRaw records.
        - Enforce transactional integrity.
        - Delegate all persistence to the repository.
    """

    def __init__(
        self,
        repository: AIResultRawRepository | None = None,
    ) -> None:
        self._repository = repository or AIResultRawRepository()

    @transaction.atomic
    def persist(
        self,
        *,
        inspection: Inspection,
        payload: dict,
    ) -> AIResultRaw:
        """
        Persist a validated AI payload.

        Assumptions:
            - Payload has already been validated by AIContractValidator.
            - inspection exists.

        Raises:
            DuplicateAIResultError
        """

        return self._repository.create(
            inspection=inspection,
            inspection_run_id=payload["inspection_run_id"],
            status=payload["status"],
            payload=payload,
        )