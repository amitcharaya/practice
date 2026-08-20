from django.conf import settings
from django.db import models


class AuditLog(models.Model):

    class Action(models.TextChoices):
        CREATE = "CREATE", "Create"
        UPDATE = "UPDATE", "Update"
        DELETE = "DELETE", "Delete"
        SUBMIT = "SUBMIT", "Submit"
        ACCEPT = "ACCEPT", "Accept"
        REJECT = "REJECT", "Reject"
        VERIFY = "VERIFY", "Verify"
        APPROVE = "APPROVE", "Approve"
        RETURN = "RETURN", "Return"
        CANCEL = "CANCEL", "Cancel"
        TREASURY_SUBMIT = "TREASURY_SUBMIT", "Submitted to Treasury"
        LOGIN = "LOGIN", "Login"
        LOGOUT = "LOGOUT", "Logout"
        UPLOAD = "UPLOAD", "Upload"
        DOWNLOAD = "DOWNLOAD", "Download"
        EXPORT = "EXPORT", "Export"
        OTHER = "OTHER", "Other"

    class Module(models.TextChoices):
        USERS = "USERS", "Users"
        MASTER_DATA = "MASTER_DATA", "Master Data"
        SUPPLY_CHAIN = "SUPPLY_CHAIN", "Supply Chain"
        AUDIT = "AUDIT", "Audit"
        REPORTING = "REPORTING", "Reporting"
        SYSTEM = "SYSTEM", "System"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="audit_logs",
    )

    action = models.CharField(
        max_length=50,
        choices=Action.choices,
    )

    module = models.CharField(
        max_length=50,
        choices=Module.choices,
    )

    object_type = models.CharField(
        max_length=100,
    )

    object_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    from_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    to_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        default="",
    )

    changes = models.JSONField(
        blank=True,
        null=True,
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    user_agent = models.TextField(
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        db_table = "audit_log"
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["module", "created_at"]
            ),
            models.Index(
                fields=["object_type", "object_id"]
            ),
            models.Index(
                fields=["user", "created_at"]
            ),
            models.Index(
                fields=["action", "created_at"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.user} - "
            f"{self.action} - "
            f"{self.object_type} - "
            f"{self.object_id}"
        )