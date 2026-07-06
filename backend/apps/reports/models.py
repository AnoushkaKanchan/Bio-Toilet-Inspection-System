import uuid

from django.db import models

from apps.inspection.models import Inspection


class Report(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    inspection = models.OneToOneField(
        Inspection,
        on_delete=models.CASCADE,
        related_name="report",
    )

    report_path = models.CharField(
        max_length=500,
        help_text="Path to the generated inspection report.",
    )

    generated_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "report"
        ordering = ["-generated_at"]
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self):
        return f"Report - {self.inspection.train_number}"
