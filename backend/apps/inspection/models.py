import uuid

from django.db import models


class InspectionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"


class Inspection(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    train_number = models.CharField(max_length=20)

    pit_line_number = models.CharField(max_length=20)

    inspection_time = models.DateTimeField(
        help_text="Timestamp when the inspection session begins."
    )

    status = models.CharField(
        max_length=20,
        choices=InspectionStatus.choices,
        default=InspectionStatus.PENDING,
    )

    total_coaches = models.PositiveIntegerField(default=0)

    total_tanks = models.PositiveIntegerField(default=0)

    total_defected_tanks = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inspection"
        ordering = ["-created_at"]
        verbose_name = "Inspection"
        verbose_name_plural = "Inspections"

    def __str__(self):
        return f"{self.train_number} - {self.status}"
