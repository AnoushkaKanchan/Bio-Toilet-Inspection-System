from django.contrib import admin

from .models import AIResultRaw


@admin.register(AIResultRaw)
class AIResultRawAdmin(admin.ModelAdmin):
    list_display = (
        "inspection",
        "received_at",
    )

    search_fields = ("inspection__train_number",)

    list_filter = ("received_at",)

    readonly_fields = (
        "id",
        "payload",
        "received_at",
    )

    ordering = ("-received_at",)
