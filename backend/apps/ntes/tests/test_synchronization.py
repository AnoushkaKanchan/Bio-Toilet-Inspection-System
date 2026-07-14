from contextlib import nullcontext
from unittest.mock import Mock, patch

import pytest

from apps.ntes.services.synchronization import (
    SynchronizationService,
)

pytestmark = pytest.mark.django_db


def create_service():
    dependencies = {
        "client": Mock(),
        "parser": Mock(),
        "normalizer": Mock(),
        "repository": Mock(),
        "verifier": Mock(),
        "ai_repository": Mock(),
        "mapping_workflow": Mock(),
    }

    with patch(
        "apps.ntes.services.synchronization.transaction.atomic",
        return_value=nullcontext(),
    ):
        service = SynchronizationService(
            client=dependencies["client"],
            parser=dependencies["parser"],
            normalizer=dependencies["normalizer"],
            repository=dependencies["repository"],
            verifier=dependencies["verifier"],
            ai_repository=dependencies["ai_repository"],
            mapping_workflow=dependencies["mapping_workflow"],
        )

    return service, dependencies


def test_synchronize_success():
    service, deps = create_service()

    inspection = Mock()
    inspection.id = 1
    inspection.train_number = "12951"

    html = "<html></html>"
    raw = [Mock()]
    dtos = [Mock()]
    coaches = [Mock()]

    deps["client"].fetch.return_value = html
    deps["parser"].parse.return_value = raw
    deps["normalizer"].normalize.return_value = dtos
    deps["verifier"].verify.return_value = coaches
    deps["ai_repository"].get_latest_by_inspection.return_value = None

    result = service.synchronize(
        inspection=inspection,
    )

    deps["client"].fetch.assert_called_once_with(
        train_number="12951",
    )

    deps["parser"].parse.assert_called_once_with(
        html=html,
    )

    deps["normalizer"].normalize.assert_called_once_with(
        coaches=raw,
    )

    deps["repository"].replace_composition.assert_called_once_with(
        inspection=inspection,
        coaches=dtos,
    )

    deps["verifier"].verify.assert_called_once_with(
        inspection=inspection,
    )

    deps["ai_repository"].get_latest_by_inspection.assert_called_once_with(
        inspection=inspection,
    )

    deps["mapping_workflow"].execute.assert_not_called()

    assert result == coaches


def test_mapping_workflow_runs_when_ai_exists():
    service, deps = create_service()

    inspection = Mock()
    inspection.id = 1
    inspection.train_number = "12951"

    html = "<html></html>"
    raw = [Mock()]
    dtos = [Mock()]
    coaches = [Mock()]

    ai_result = Mock()
    ai_result.payload = {
        "inspection_run_id": "run-1",
    }

    deps["client"].fetch.return_value = html
    deps["parser"].parse.return_value = raw
    deps["normalizer"].normalize.return_value = dtos
    deps["verifier"].verify.return_value = coaches
    deps["ai_repository"].get_latest_by_inspection.return_value = ai_result

    service.synchronize(
        inspection=inspection,
    )

    deps["mapping_workflow"].execute.assert_called_once_with(
        inspection=inspection,
        payload=ai_result.payload,
        coaches=coaches,
    )


def test_mapping_workflow_skipped_when_ai_missing():
    service, deps = create_service()

    inspection = Mock()
    inspection.id = 1
    inspection.train_number = "12951"

    html = "<html></html>"
    raw = [Mock()]
    dtos = [Mock()]
    coaches = [Mock()]

    deps["client"].fetch.return_value = html
    deps["parser"].parse.return_value = raw
    deps["normalizer"].normalize.return_value = dtos
    deps["verifier"].verify.return_value = coaches
    deps["ai_repository"].get_latest_by_inspection.return_value = None

    service.synchronize(
        inspection=inspection,
    )

    deps["mapping_workflow"].execute.assert_not_called()


@pytest.mark.parametrize(
    "stage",
    [
        "client",
        "parser",
        "normalizer",
        "repository",
        "verifier",
    ],
)
def test_pipeline_stops_on_failure(stage):
    service, deps = create_service()

    inspection = Mock()
    inspection.id = 1
    inspection.train_number = "12951"

    html = "<html></html>"
    raw = [Mock()]
    dtos = [Mock()]

    deps["client"].fetch.return_value = html
    deps["parser"].parse.return_value = raw
    deps["normalizer"].normalize.return_value = dtos

    failure = RuntimeError("failure")

    if stage == "client":
        deps["client"].fetch.side_effect = failure

    elif stage == "parser":
        deps["parser"].parse.side_effect = failure

    elif stage == "normalizer":
        deps["normalizer"].normalize.side_effect = failure

    elif stage == "repository":
        deps["repository"].replace_composition.side_effect = failure

    else:
        deps["verifier"].verify.side_effect = failure

    with pytest.raises(RuntimeError):
        service.synchronize(
            inspection=inspection,
        )

    if stage == "client":
        deps["parser"].parse.assert_not_called()
        deps["normalizer"].normalize.assert_not_called()
        deps["repository"].replace_composition.assert_not_called()
        deps["verifier"].verify.assert_not_called()

    elif stage == "parser":
        deps["normalizer"].normalize.assert_not_called()
        deps["repository"].replace_composition.assert_not_called()
        deps["verifier"].verify.assert_not_called()

    elif stage == "normalizer":
        deps["repository"].replace_composition.assert_not_called()
        deps["verifier"].verify.assert_not_called()

    elif stage == "repository":
        deps["verifier"].verify.assert_not_called()