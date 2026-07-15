import re

TOP_LEVEL_REQUIRED_FIELDS = (
    "inspection_run_id",
    "processing_timestamp",
    "status",
    "tanks",
)

TANK_REQUIRED_FIELDS = (
    "coach_number",
    "tank_id",
    "camera_side",
    "timestamp_sec",
    "pipe_status",
    "pipe_support_status",
    "surface_status",
    "maintenance_status",
    "detection_confidence",
    "tank_image_path",
)

OPTIONAL_TANK_FIELDS = (
    "synced_tank_id",
)

# Centralized Tank ID regex validation pattern (e.g., L1, R2, L10)
TANK_ID_PATTERN = re.compile(r"^[LR]\d+$")

# Immutable configuration constants
VALID_CAMERA_SIDES = frozenset({
    "LEFT",
    "RIGHT",
})

VALID_PIPE_STATUS = frozenset({
    "Connected",
    "Not Connected",
})

VALID_PIPE_SUPPORT_STATUS = frozenset({
    "Present",
    "Absent",
})

VALID_SURFACE_STATUS = frozenset({
    "Clean",
    "Not Clean",
})

VALID_MAINTENANCE_STATUS = frozenset({
    "Normal",
    "Maintenance Required",
})

VALID_RUN_STATUS = frozenset({
    "COMPLETE",
})

ALLOWED_TOP_LEVEL_FIELDS = frozenset(
    TOP_LEVEL_REQUIRED_FIELDS,
)

ALLOWED_TANK_FIELDS = (
    frozenset(TANK_REQUIRED_FIELDS)
    | frozenset(OPTIONAL_TANK_FIELDS)
)