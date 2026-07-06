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


class CameraSide(models.TextChoices):
    LEFT = "LEFT", "Left"
    RIGHT = "RIGHT", "Right"


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


class Tank(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    coach = models.ForeignKey(
        Coach,
        on_delete=models.CASCADE,
        related_name="tanks",
    )

    tank_index = models.PositiveIntegerField(
        help_text=(
            "Global tank index assigned by the AI for the entire inspection. "
            "Uniqueness is enforced by the Mapping Engine."
        ),
    )

    camera = models.CharField(
        max_length=5,
        choices=CameraSide.choices,
    )

    timestamp_seconds = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        help_text="Timestamp (in seconds) within the inspection video.",
    )

    confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="AI confidence score.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "tank"
        ordering = ["tank_index"]
        verbose_name = "Tank"
        verbose_name_plural = "Tanks"

    def __str__(self):
        return f"Tank {self.tank_index} ({self.camera})"


class TankDefect(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    tank = models.ForeignKey(
        Tank,
        on_delete=models.CASCADE,
        related_name="defects",
    )

    defect_type = models.CharField(
        max_length=100,
        help_text="Raw defect label returned by the AI service.",
    )

    confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="AI confidence score for the detected defect.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "tank_defect"
        ordering = ["id"]
        verbose_name = "Tank Defect"
        verbose_name_plural = "Tank Defects"

    def __str__(self):
        return f"{self.defect_type} ({self.confidence}%)"
