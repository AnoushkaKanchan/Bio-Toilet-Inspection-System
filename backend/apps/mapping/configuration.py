from apps.mapping.enums import TankDefectType

AI_STATUS_TO_DEFECT = {
    (
        "pipe_status",
        "Not Connected",
    ): TankDefectType.PIPE_NOT_CONNECTED,
    (
        "pipe_support_status",
        "Absent",
    ): TankDefectType.PIPE_SUPPORT_ABSENT,
    (
        "surface_status",
        "Not Clean",
    ): TankDefectType.SURFACE_NOT_CLEAN,
}
