import uuid

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from apps.inspection.models import Inspection


class AIResultRaw(models.Model):
    """
    Immutable integration record.

    Stores the raw AI payload exactly as received.
    Business services must never modify the payload after creation.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    inspection = models.ForeignKey(
        Inspection,
        on_delete=models.CASCADE,
        related_name="ai_results",
    )

    inspection_run_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    payload = models.JSONField(
        encoder=DjangoJSONEncoder,
        help_text=(
            "Immutable raw JSON payload received from the AI service. "
            "Must never be modified after creation."
        ),
    )

    received_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "ai_result_raw"
        ordering = ["-received_at"]
        indexes = [
            models.Index(fields=["inspection"]),
            models.Index(fields=["received_at"]),
        ]
        verbose_name = "AI Result"
        verbose_name_plural = "AI Results"

    def __str__(self):
        return f"AI Result - {self.inspection.train_number}"
