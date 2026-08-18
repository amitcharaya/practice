from .models import AuditLog
def create_audit_log(
    *,
    user,
    action,
    module,
    object_type,
    object_id,
    from_status=None,
    to_status=None,
    description="",
    changes=None,
):

    return AuditLog.objects.create(
        user=user,
        action=action,
        module=module,
        object_type=object_type,
        object_id=str(object_id),
        from_status=from_status,
        to_status=to_status,
        description=description,
        changes=changes,
    )