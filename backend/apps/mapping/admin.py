from django.contrib import admin

from .models import Coach, Tank, TankDefect


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = (
        "physical_sequence",
        "ntes_coach",
        "mapping_status",
        "coach_inspection_status",
        "inspection",
    )

    list_filter = (
        "mapping_status",
        "coach_inspection_status",
    )

    search_fields = ("ntes_coach__coach_number",)

    ordering = ("physical_sequence",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Tank)
class TankAdmin(admin.ModelAdmin):
    list_display = (
        "tank_index",
        "coach",
        "camera",
        "confidence",
    )

    list_filter = ("camera",)

    search_fields = ("coach__ntes_coach__coach_number",)

    ordering = (
        "coach__physical_sequence",
        "tank_index",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(TankDefect)
class TankDefectAdmin(admin.ModelAdmin):
    list_display = (
        "tank",
        "defect_type",
        "confidence",
    )

    list_filter = ("defect_type",)

    search_fields = (
        "defect_type",
        "tank__coach__ntes_coach__coach_number",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at"
    )
