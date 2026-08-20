from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "user",
        "action",
        "module",
        "object_type",
        "object_id",
        "from_status",
        "to_status",
        "created_at",
    ]

    list_filter = [
        "action",
        "module",
        "object_type",
        "created_at",
    ]

    search_fields = [
        "user__username",
        "object_type",
        "object_id",
        "description",
    ]

    readonly_fields = [
        "user",
        "action",
        "module",
        "object_type",
        "object_id",
        "from_status",
        "to_status",
        "description",
        "changes",
        "ip_address",
        "user_agent",
        "created_at",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(
        self,
        request,
        obj=None
    ):
        return False

    def has_delete_permission(
        self,
        request,
        obj=None
    ):
        return False