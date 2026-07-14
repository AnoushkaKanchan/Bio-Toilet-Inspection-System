from django.contrib import admin

from .models import Inspection


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = (
        "train_number",
        "pit_line_number",
        "status",
        "inspection_time",
        "total_coaches",
        "total_tanks",
        "total_defected_tanks",
    )

    list_filter = (
        "status",
        "inspection_time",
    )

    search_fields = (
        "train_number",
        "pit_line_number",
    )

    ordering = ("-inspection_time",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
