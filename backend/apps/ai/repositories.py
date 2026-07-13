from django.db import IntegrityError

from apps.ai.exceptions import (
    AIPersistenceError,
    AIResultNotFoundError,
    DuplicateAIResultError,
)
from apps.ai.models import AIResultRaw
from apps.inspection.models import Inspection


class AIResultRawRepository:
    """
    Repository responsible for persistence of immutable AIResultRaw records.

    This repository is the exclusive persistence boundary for AIResultRaw.
    """

    def create(
        self,
        *,
        inspection: Inspection,
        inspection_run_id: str,
        status: str,
        payload: dict,
    ) -> AIResultRaw:
        """
        Persist a new immutable AI payload.

        Raises:
            DuplicateAIResultError:
                If the inspection_run_id already exists.
        """
        try:
            return AIResultRaw.objects.create(
                inspection=inspection,
                inspection_run_id=inspection_run_id,
                status=status,
                payload=payload,
            )

        except IntegrityError as exc:
            raise DuplicateAIResultError(
                f"AI result '{inspection_run_id}' already exists."
            ) from exc

        except Exception as exc:
            raise AIPersistenceError(
                "Failed to persist AI result."
            ) from exc

    def get_by_inspection_run_id(
        self,
        *,
        inspection_run_id: str,
    ) -> AIResultRaw:
        """
        Retrieve a persisted AI result.

        Raises:
            AIResultNotFoundError
        """
        try:
            return AIResultRaw.objects.get(
                inspection_run_id=inspection_run_id,
            )

        except AIResultRaw.DoesNotExist as exc:
            raise AIResultNotFoundError(
                f"AI result '{inspection_run_id}' does not exist."
            ) from exc

    def exists(
        self,
        *,
        inspection_run_id: str,
    ) -> bool:
        """
        Check whether an AI inspection run has already been stored.
        """
        return AIResultRaw.objects.filter(
            inspection_run_id=inspection_run_id,
        ).exists()

    def get_by_inspection(
        self,
        *,
        inspection: Inspection,
    ) -> list[AIResultRaw]:
        """
        Retrieve all AI results belonging to an inspection.

        Results are ordered newest first according to the model Meta.
        """
        return list(
            AIResultRaw.objects.filter(
                inspection=inspection,
            )
        )