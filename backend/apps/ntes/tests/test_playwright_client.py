import pytest

from apps.ntes.clients import PlaywrightNTESClient
from apps.ntes.exceptions import (
    CoachCompositionNotFoundError,
    NTESClientTimeoutError,
    NTESUnavailableError,
    TrainNotFoundError,
)


@pytest.fixture
def client():
    return PlaywrightNTESClient()


def test_fetch_returns_modal_html(
    monkeypatch,
    client,
):
    expected_html = "<div>Coach Position</div>"

    monkeypatch.setattr(
        client,
        "_launch_browser",
        lambda: (None, None, None, object()),
    )

    monkeypatch.setattr(
        client,
        "_open_ntes",
        lambda page: None,
    )

    monkeypatch.setattr(
        client,
        "_search_train",
        lambda page, train: None,
    )

    monkeypatch.setattr(
        client,
        "_check_invalid_train",
        lambda page: None,
    )

    monkeypatch.setattr(
        client,
        "_open_coach_position",
        lambda page: None,
    )

    monkeypatch.setattr(
        client,
        "_extract_modal_html",
        lambda page: expected_html,
    )

    monkeypatch.setattr(
        client,
        "_cleanup",
        lambda *args: None,
    )

    html = client.fetch(
        train_number="12951",
    )

    assert html == expected_html


def test_invalid_train_raises_exception(
    monkeypatch,
    client,
):
    monkeypatch.setattr(
        client,
        "_launch_browser",
        lambda: (None, None, None, object()),
    )

    monkeypatch.setattr(
        client,
        "_open_ntes",
        lambda page: None,
    )

    monkeypatch.setattr(
        client,
        "_search_train",
        lambda page, train: None,
    )

    monkeypatch.setattr(
        client,
        "_check_invalid_train",
        lambda page: ((_ for _ in ()).throw(TrainNotFoundError())),
    )

    monkeypatch.setattr(
        client,
        "_cleanup",
        lambda *args: None,
    )

    with pytest.raises(
        TrainNotFoundError,
    ):
        client.fetch(
            train_number="99999",
        )


def test_missing_coach_position(
    monkeypatch,
    client,
):
    monkeypatch.setattr(
        client,
        "_launch_browser",
        lambda: (None, None, None, object()),
    )

    monkeypatch.setattr(
        client,
        "_open_ntes",
        lambda page: None,
    )

    monkeypatch.setattr(
        client,
        "_search_train",
        lambda page, train: None,
    )

    monkeypatch.setattr(
        client,
        "_check_invalid_train",
        lambda page: None,
    )

    monkeypatch.setattr(
        client,
        "_open_coach_position",
        lambda page: ((_ for _ in ()).throw(CoachCompositionNotFoundError())),
    )

    monkeypatch.setattr(
        client,
        "_cleanup",
        lambda *args: None,
    )

    with pytest.raises(
        CoachCompositionNotFoundError,
    ):
        client.fetch(
            train_number="12951",
        )


def test_timeout(
    monkeypatch,
    client,
):
    monkeypatch.setattr(
        client,
        "_launch_browser",
        lambda: ((_ for _ in ()).throw(NTESClientTimeoutError())),
    )

    monkeypatch.setattr(
        client,
        "_cleanup",
        lambda *args: None,
    )

    with pytest.raises(
        NTESClientTimeoutError,
    ):
        client.fetch(
            train_number="12951",
        )


def test_ntes_unavailable(
    monkeypatch,
    client,
):
    monkeypatch.setattr(
        client,
        "_launch_browser",
        lambda: ((_ for _ in ()).throw(RuntimeError())),
    )

    monkeypatch.setattr(
        client,
        "_cleanup",
        lambda *args: None,
    )

    with pytest.raises(
        NTESUnavailableError,
    ):
        client.fetch(
            train_number="12951",
        )


def test_cleanup_called_on_exception(
    monkeypatch,
    client,
):
    cleanup_called = False

    def cleanup(*args):
        nonlocal cleanup_called
        cleanup_called = True

    monkeypatch.setattr(
        client,
        "_launch_browser",
        lambda: ((_ for _ in ()).throw(RuntimeError())),
    )

    monkeypatch.setattr(
        client,
        "_cleanup",
        cleanup,
    )

    with pytest.raises(
        NTESUnavailableError,
    ):
        client.fetch(
            train_number="12951",
        )

    assert cleanup_called
