import pytest

from apps.ai.exceptions import (
    DuplicateAIResultError,
)
from apps.ai.models import AIResultRaw
from apps.ai.repositories import AIResultRawRepository
from apps.ai.services.persistence import (
    AIResultPersistenceService,
)


@pytest.mark.django_db
class TestAIResultPersistenceService:

    @pytest.fixture
    def repository(self):
        return AIResultRawRepository()

    @pytest.fixture
    def service(self, repository):
        return AIResultPersistenceService(
            repository=repository,
        )

    @pytest.fixture
    def payload(self):
        return {
            "inspection_run_id": "run-001",
            "status": "COMPLETE",
            "train_inspection_timestamp": "2026-07-13T12:30:00Z",
            "video_source": "left.mp4",
            "summary": {},
            "tanks": [],
        }

    def test_persist(
        self,
        service,
        inspection,
        payload,
    ):
        result = service.persist(
            inspection=inspection,
            payload=payload,
        )

        assert isinstance(result, AIResultRaw)

        assert result.inspection == inspection
        assert result.inspection_run_id == "run-001"
        assert result.status == "COMPLETE"
        assert result.payload == payload

    def test_duplicate_ai_result(
        self,
        service,
        inspection,
        payload,
    ):
        service.persist(
            inspection=inspection,
            payload=payload,
        )

        with pytest.raises(
            DuplicateAIResultError,
        ):
            service.persist(
                inspection=inspection,
                payload=payload,
            )

    def test_multiple_ai_results(
        self,
        service,
        inspection,
        payload,
    ):
        service.persist(
            inspection=inspection,
            payload=payload,
        )

        second = {
            **payload,
            "inspection_run_id": "run-002",
        }

        service.persist(
            inspection=inspection,
            payload=second,
        )

        assert AIResultRaw.objects.count() == 2