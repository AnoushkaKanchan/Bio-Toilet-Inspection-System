from pathlib import Path
from unittest.mock import Mock

import pytest

from django.utils import timezone
from apps.inspection.models import Inspection
from apps.inspection.repositories import InspectionRepository
from apps.inspection.services import InspectionWorkflowService
from apps.ntes.normalizer import NTESNormalizer
from apps.ntes.parser import NTESHTMLParser
from apps.ntes.repositories import NTESCoachRepository
from apps.ntes.services import (
    NTESVerificationService,
    SynchronizationService,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def inspection():
    return Inspection.objects.create(
        train_number="12951",
        pit_line_number="P1",
        inspection_time=timezone.now(),
    )


@pytest.fixture
def coach_html():
    fixture = (
        Path(__file__).parents[2]
        / "ntes"
        / "tests"
        / "fixtures"
        / "coach_position.html"
    )

    return fixture.read_text(
        encoding="utf-8",
    )


@pytest.fixture
def client(
    coach_html,
):
    client = Mock()

    client.fetch.return_value = coach_html

    return client


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


@pytest.fixture
def workflow_service(
    synchronization_service,
):
    return InspectionWorkflowService(
        repository=InspectionRepository(),
        synchronization_service=synchronization_service,
    )
