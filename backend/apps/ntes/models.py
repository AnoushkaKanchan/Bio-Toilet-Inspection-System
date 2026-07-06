import uuid

from django.db import models

from apps.inspection.models import Inspection


class NTESCoach(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    inspection = models.ForeignKey(
        Inspection,
        on_delete=models.CASCADE,
        related_name="ntes_coaches",
    )

    coach_sequence = models.PositiveIntegerField()

    coach_number = models.CharField(
        max_length=20,
    )

    coach_type = models.CharField(
        max_length=20,
        help_text="Raw coach type code received from NTES.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "ntes_coach"
        ordering = ["coach_sequence"]
        verbose_name = "NTES Coach"
        verbose_name_plural = "NTES Coaches"

    def __str__(self):
        return f"{self.coach_sequence} - {self.coach_number}"
