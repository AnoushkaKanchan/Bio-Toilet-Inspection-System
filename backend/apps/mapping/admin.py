from django.contrib import admin

from .models import Coach


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
