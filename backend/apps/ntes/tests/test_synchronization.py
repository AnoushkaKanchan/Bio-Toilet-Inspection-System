from contextlib import nullcontext
from unittest.mock import Mock, patch
import pytest

pytestmark = pytest.mark.django_db

from apps.ntes.services.synchronization import (
    SynchronizationService,
)


@pytest.fixture
def dependencies():
    return {
        "client": Mock(),
        "parser": Mock(),
        "normalizer": Mock(),
        "repository": Mock(),
        "verifier": Mock(),
    }


@pytest.fixture
def service(
    dependencies,
):
    with patch(
        "apps.ntes.services.synchronization.transaction.atomic",
        return_value=nullcontext(),
    ):
        yield SynchronizationService(
            client=dependencies["client"],
            parser=dependencies["parser"],
            normalizer=dependencies["normalizer"],
            repository=dependencies["repository"],
            verifier=dependencies["verifier"],
        )


def test_synchronize_success(
    service,
    dependencies,
):
    inspection = Mock()
    inspection.id = 1
    inspection.train_number = "12951"

    html = "<html></html>"
    raw = [Mock()]
    dtos = [Mock()]
    coaches = [Mock()]

    dependencies["client"].fetch.return_value = html
    dependencies["parser"].parse.return_value = raw
    dependencies["normalizer"].normalize.return_value = dtos
    dependencies["repository"].replace_composition.return_value = []
    dependencies["verifier"].verify.return_value = coaches

    result = service.synchronize(
        inspection=inspection,
    )

    dependencies["client"].fetch.assert_called_once_with(
        train_number="12951",
    )
    dependencies["parser"].parse.assert_called_once_with(
        html=html,
    )
    dependencies["normalizer"].normalize.assert_called_once_with(
        coaches=raw,
    )
    dependencies["repository"].replace_composition.assert_called_once_with(
        inspection=inspection,
        coaches=dtos,
    )
    dependencies["verifier"].verify.assert_called_once_with(
        inspection=inspection,
    )

    assert result == coaches


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
def test_pipeline_stops_on_failure(
    service,
    dependencies,
    stage,
):
    inspection = Mock()
    inspection.id = 1
    inspection.train_number = "12951"

    html = "<html></html>"
    raw = [Mock()]
    dtos = [Mock()]

    dependencies["client"].fetch.return_value = html
    dependencies["parser"].parse.return_value = raw
    dependencies["normalizer"].normalize.return_value = dtos

    failure = RuntimeError("failure")

    if stage == "client":
        dependencies["client"].fetch.side_effect = failure

    elif stage == "parser":
        dependencies["parser"].parse.side_effect = failure

    elif stage == "normalizer":
        dependencies["normalizer"].normalize.side_effect = failure

    elif stage == "repository":
        dependencies["repository"].replace_composition.side_effect = failure

    else:
        dependencies["verifier"].verify.side_effect = failure

    with pytest.raises(RuntimeError):
        service.synchronize(
            inspection=inspection,
        )

    if stage == "client":
        dependencies["parser"].parse.assert_not_called()
        dependencies["normalizer"].normalize.assert_not_called()
        dependencies["repository"].replace_composition.assert_not_called()
        dependencies["verifier"].verify.assert_not_called()

    elif stage == "parser":
        dependencies["normalizer"].normalize.assert_not_called()
        dependencies["repository"].replace_composition.assert_not_called()
        dependencies["verifier"].verify.assert_not_called()

    elif stage == "normalizer":
        dependencies["repository"].replace_composition.assert_not_called()
        dependencies["verifier"].verify.assert_not_called()

    elif stage == "repository":
        dependencies["verifier"].verify.assert_not_called()
