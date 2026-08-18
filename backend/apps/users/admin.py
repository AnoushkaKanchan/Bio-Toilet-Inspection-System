from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.users.models import OTP, HierarchyNode, Pit, User


@admin.register(HierarchyNode)
class HierarchyNodeAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "code", "parent", "active"]
    list_filter = ["type", "active"]
    search_fields = ["name", "code"]


@admin.register(Pit)
class PitAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "depot", "active"]
    list_filter = ["active"]
    search_fields = ["name", "code"]


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ["name", "email", "mobile", "role", "assigned_node", "is_active"]
    list_filter = ["role", "is_active"]
    search_fields = ["name", "email", "mobile"]
    ordering = ["name"]
    fieldsets = None
    add_fieldsets = None
    filter_horizontal = ["assigned_pits", "groups", "user_permissions"]


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ["identifier", "purpose", "attempts", "expires_at", "consumed_at"]
    list_filter = ["purpose"]