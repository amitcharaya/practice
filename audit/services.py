from .models import AuditLog


def get_client_ip(request):
    """
    Get client IP address from the request.
    """

    if request is None:
        return None

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def create_audit_log(
    *,
    user,
    action,
    module,
    object_type,
    object_id=None,
    from_status=None,
    to_status=None,
    description="",
    changes=None,
    request=None,
):
    """
    Centralized audit logging service.
    """

    ip_address = get_client_ip(request)

    user_agent = ""

    if request:
        user_agent = request.META.get(
            "HTTP_USER_AGENT",
            ""
        )

    return AuditLog.objects.create(
        user=user,
        action=action,
        module=module,
        object_type=object_type,
        object_id=str(object_id) if object_id is not None else None,
        from_status=from_status,
        to_status=to_status,
        description=description,
        changes=changes,
        ip_address=ip_address,
        user_agent=user_agent,
    )