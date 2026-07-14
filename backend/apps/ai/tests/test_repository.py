import pytest

from apps.ai.exceptions import (
    AIResultNotFoundError,
    DuplicateAIResultError,
)
from apps.ai.models import AIResultRaw
from apps.ai.repositories import AIResultRawRepository


@pytest.mark.django_db
class TestAIResultRawRepository:
    @pytest.fixture
    def repository(self):
        return AIResultRawRepository()

    @pytest.fixture
    def payload(self):
        return {
            "inspection_run_id": "run-001",
            "status": "COMPLETE",
            "video_source": "left_camera.mp4",
            "train_inspection_timestamp": "2026-07-13T10:30:00Z",
            "summary": {},
            "tanks": [],
        }

    def test_create(
        self,
        repository,
        inspection,
        payload,
    ):
        result = repository.create(
            inspection=inspection,
            inspection_run_id=payload["inspection_run_id"],
            status=payload["status"],
            payload=payload,
        )

        assert isinstance(result, AIResultRaw)

        assert result.inspection == inspection
        assert result.inspection_run_id == "run-001"
        assert result.status == "COMPLETE"
        assert result.payload == payload

    def test_exists_returns_true(
        self,
        repository,
        inspection,
        payload,
    ):
        repository.create(
            inspection=inspection,
            inspection_run_id=payload["inspection_run_id"],
            status=payload["status"],
            payload=payload,
        )

        assert repository.exists(
            inspection_run_id="run-001",
        )

    def test_exists_returns_false(
        self,
        repository,
    ):
        assert not repository.exists(
            inspection_run_id="missing",
        )

    def test_get_by_inspection_run_id(
        self,
        repository,
        inspection,
        payload,
    ):
        created = repository.create(
            inspection=inspection,
            inspection_run_id=payload["inspection_run_id"],
            status=payload["status"],
            payload=payload,
        )

        fetched = repository.get_by_inspection_run_id(
            inspection_run_id="run-001",
        )

        assert fetched == created

    def test_get_by_inspection_run_id_not_found(
        self,
        repository,
    ):
        with pytest.raises(AIResultNotFoundError):
            repository.get_by_inspection_run_id(
                inspection_run_id="missing",
            )

    def test_duplicate_inspection_run_id(
        self,
        repository,
        inspection,
        payload,
    ):
        repository.create(
            inspection=inspection,
            inspection_run_id="run-001",
            status=payload["status"],
            payload=payload,
        )

        with pytest.raises(DuplicateAIResultError):
            repository.create(
                inspection=inspection,
                inspection_run_id="run-001",
                status=payload["status"],
                payload=payload,
            )

    def test_get_by_inspection(
        self,
        repository,
        inspection,
        payload,
    ):
        repository.create(
            inspection=inspection,
            inspection_run_id="run-001",
            status=payload["status"],
            payload=payload,
        )

        repository.create(
            inspection=inspection,
            inspection_run_id="run-002",
            status=payload["status"],
            payload={
                **payload,
                "inspection_run_id": "run-002",
            },
        )

        results = repository.get_by_inspection(
            inspection=inspection,
        )

        assert len(results) == 2

        assert all(
            result.inspection == inspection
            for result in results
        )