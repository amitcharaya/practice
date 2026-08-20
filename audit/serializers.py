from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(
    serializers.ModelSerializer
):

    user_name = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = AuditLog

        fields = [
            "id",
            "user",
            "user_name",
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

        read_only_fields = fields