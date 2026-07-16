from django.db import transaction

from apps.ai.repositories import AIResultRawRepository
from apps.inspection.repositories import InspectionRepository
from apps.ntes.dto import FetchTrainResponseDTO
from apps.ntes.services.synchronization import (
    SynchronizationService,
)
from apps.inspection.models import InspectionStatus


class FetchTrainService:

    def __init__(
        self,
        *,
        inspection_repository=None,
        synchronization_service=None,
        ai_repository=None,
    ):
        self._inspection_repository = (
            inspection_repository
            or InspectionRepository()
        )

        self._synchronization_service = (
            synchronization_service
            or SynchronizationService()
        )

        self._ai_repository = (
            ai_repository
            or AIResultRawRepository()
        )

    @transaction.atomic
    def fetch(self, *, inspection_id, train_number) -> FetchTrainResponseDTO:
        inspection = self._inspection_repository.get(inspection_id=inspection_id)
        inspection = self._inspection_repository.assign_train(
            inspection=inspection,
            train_number=train_number,
        )
        coaches = self._synchronization_service.synchronize(inspection=inspection)

        inspection.status = InspectionStatus.COMPLETED
        self._inspection_repository.save(inspection=inspection)

        mapping_executed = (
            self._ai_repository.get_latest_by_inspection(inspection=inspection)
            is not None
        )

        return FetchTrainResponseDTO(
            success=True,
            inspection_id=str(inspection.id),
            coaches_synchronized=len(coaches),
            mapping_executed=mapping_executed,
            train_number=inspection.train_number,
            train_name=inspection.train_name,      
        )