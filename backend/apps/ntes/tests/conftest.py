from pathlib import Path
from unittest.mock import Mock

import pytest
from django.utils import timezone

from apps.inspection.models import Inspection
from apps.ntes.normalizer import NTESNormalizer
from apps.ntes.parser import NTESHTMLParser
from apps.ntes.repositories import NTESCoachRepository
from apps.ntes.services import (
    NTESVerificationService,
    SynchronizationService,
)


@pytest.fixture
def coach_html() -> str:
    fixture = Path(__file__).parent / "fixtures" / "coach_position.html"

    return fixture.read_text(
        encoding="utf-8",
    )


@pytest.fixture
def inspection(db):
    return Inspection.objects.create(
        train_number="12951",
        pit_line_number="P1",
        inspection_time=timezone.now(),
    )


@pytest.fixture
def repository():
    return NTESCoachRepository()


@pytest.fixture
def parser():
    return NTESHTMLParser()


@pytest.fixture
def normalizer():
    return NTESNormalizer()


@pytest.fixture
def verifier(
    repository,
):
    return NTESVerificationService(
        repository=repository,
    )


@pytest.fixture
def client(
    coach_html,
):
    client = Mock()
    client.fetch.return_value = coach_html
    return client


@pytest.fixture
def synchronization_service(
    client,
    parser,
    normalizer,
    repository,
    verifier,
):
    return SynchronizationService(
        client=client,
        parser=parser,
        normalizer=normalizer,
        repository=repository,
        verifier=verifier,
    )
