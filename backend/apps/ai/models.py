import uuid

from django.db import models

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

    payload = models.JSONField(
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
