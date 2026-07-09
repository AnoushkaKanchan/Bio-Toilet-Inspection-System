TOP_LEVEL_REQUIRED_FIELDS = (
    "inspection_run_id",
    "train_inspection_timestamp",
    "video_source",
    "tanks",
    "summary",
    "status",
)

TANK_REQUIRED_FIELDS = (
    "coach_number",
    "tank_id",
    "camera_side",
    "timestamp_sec",
    "pipe_status",
    "surface_status",
    "maintenance_status",
    "detection_confidence",
    "detection_image_path",
)

OPTIONAL_TANK_FIELDS = (
    "synced_tank_id",
    "pipe_support_status",
)

VALID_CAMERA_SIDES = {
    "Left",
    "Right",
}

VALID_PIPE_STATUS = {
    "Connected",
    "Not Connected",
}

VALID_PIPE_SUPPORT_STATUS = {
    "Present",
    "Absent",
}

VALID_SURFACE_STATUS = {
    "Clean",
    "Not Clean",
}

VALID_MAINTENANCE_STATUS = {
    "Normal",
    "Maintenance Required",
}

VALID_RUN_STATUS = {
    "complete",
}
