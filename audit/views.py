

# Create your views here.
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditLog
from .serializers import AuditLogSerializer
from .permissions import IsAuditViewer


from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
)


@extend_schema_view(
    list=extend_schema(
        summary="List audit logs",
        description=(
            "Returns audit records for authorized "
            "users."
        ),
    ),
    retrieve=extend_schema(
        summary="Retrieve audit log",
        description=(
            "Returns a single immutable audit record."
        ),
    ),
)

class AuditLogViewSet(
    viewsets.ReadOnlyModelViewSet
):

    queryset = (
        AuditLog.objects
        .select_related("user")
        .all()
    )

    serializer_class = AuditLogSerializer

    permission_classes = [
        IsAuditViewer
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "user",
        "action",
        "module",
        "object_type",
        "object_id",
    ]

    search_fields = [
        "description",
        "user__username",
        "object_type",
        "object_id",
    ]

    ordering_fields = [
        "created_at",
        "action",
        "module",
    ]

    ordering = [
        "-created_at"
    ]