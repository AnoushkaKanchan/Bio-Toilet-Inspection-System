import uuid

from django.db import models

from apps.inspection.models import Inspection
from apps.ntes.models import NTESCoach


class MappingStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    MATCHED = "MATCHED", "Matched"
    UNMATCHED = "UNMATCHED", "Unmatched"
    MANUAL = "MANUAL", "Manual"


class CoachInspectionStatus(models.TextChoices):
    NORMAL = "NORMAL", "Normal"
    DEFECT = "DEFECT", "Defect"
    PARTIAL = "PARTIAL", "Partial"


class Coach(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    inspection = models.ForeignKey(
        Inspection,
        on_delete=models.CASCADE,
        related_name="coaches",
    )

    ntes_coach = models.OneToOneField(
        NTESCoach,
        on_delete=models.CASCADE,
        related_name="mapped_coach",
        null=True,
        blank=True,
    )

    physical_sequence = models.PositiveIntegerField()

    mapping_status = models.CharField(
        max_length=20,
        choices=MappingStatus.choices,
        default=MappingStatus.PENDING,
    )

    coach_inspection_status = models.CharField(
        max_length=20,
        choices=CoachInspectionStatus.choices,
        default=CoachInspectionStatus.NORMAL,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "coach"
        ordering = ["physical_sequence"]
        verbose_name = "Coach"
        verbose_name_plural = "Coaches"

    def __str__(self):
        coach_number = self.ntes_coach.coach_number if self.ntes_coach else "UNMATCHED"
        return f"{self.physical_sequence} - {coach_number}"
