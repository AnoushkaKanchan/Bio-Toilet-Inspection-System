from django.db import models


class TankDefectType(models.TextChoices):
    PIPE_NOT_CONNECTED = (
        "PIPE_NOT_CONNECTED",
        "Pipe Not Connected",
    )

    PIPE_SUPPORT_ABSENT = (
        "PIPE_SUPPORT_ABSENT",
        "Pipe Support Absent",
    )

    SURFACE_NOT_CLEAN = (
        "SURFACE_NOT_CLEAN",
        "Surface Not Clean",
    )

class CoachFilter(models.TextChoices):
    ALL = "ALL", "All"
    CLEAN = "CLEAN", "Clean"
    DEFECT = "DEFECT", "Defect"

class CoachStatus(models.TextChoices):
    CLEAN = "CLEAN", "Clean"
    DEFECT = "DEFECT", "Defect"

class CoachSideStatus(models.TextChoices):
    NORMAL = "NORMAL", "Normal"
    DEFECT = "DEFECT", "Defect"