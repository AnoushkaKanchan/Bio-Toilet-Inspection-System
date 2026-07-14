from django.contrib import admin

from .models import NTESCoach


@admin.register(NTESCoach)
class NTESCoachAdmin(admin.ModelAdmin):
    list_display = (
        "coach_sequence",
        "coach_number",
        "coach_type",
        "inspection",
    )

    search_fields = (
        "coach_number",
        "coach_type",
    )

    list_filter = ("coach_type",)

    ordering = ("coach_sequence",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
