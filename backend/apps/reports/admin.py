from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "inspection",
        "report_path",
        "generated_at",
    )

    search_fields = ("inspection__train_number",)

    ordering = ("-generated_at",)

    readonly_fields = (
        "id",
        "generated_at",
    )
