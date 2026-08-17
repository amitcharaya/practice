from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Jail, SHG, VegetableMaster
from .serializers import JailSerializer, SHGSerializer, VegetableMasterSerializer
from .permissions import IsSuperAdminOrReadOnly
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    OpenApiTypes,
)
from .services import (
    bulk_upload_jails,
    bulk_upload_shgs,
    bulk_upload_vegetables,
)


class IsSuperAdmin(permissions.BasePermission):
    """
    Allows access only to authenticated Super Admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "SA"
        )


class BulkUploadViewSet(viewsets.ViewSet):

    permission_classes = [IsSuperAdmin]
    parser_classes = [MultiPartParser]
    @extend_schema(
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "format": "binary"
                }
            },
            "required": ["file"]
        }
    },
    responses={200: OpenApiTypes.OBJECT}
    )

    @action(
        detail=False,
        methods=["post"],
        url_path="jails"
    )
    def upload_jails(self, request):

        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "Excel file is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = bulk_upload_jails(file)

        return Response(
            result,
            status=status.HTTP_200_OK
        )
    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary"
                    }
                },
                "required": ["file"]
            }
        },
        responses={200: OpenApiTypes.OBJECT}
        )
    @action(
        detail=False,
        methods=["post"],
        url_path="shgs"
    )
    def upload_shgs(self, request):

        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "Excel file is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = bulk_upload_shgs(file)

        return Response(
            result,
            status=status.HTTP_200_OK
        )
    @extend_schema(
            request={
                "multipart/form-data": {
                    "type": "object",
                    "properties": {
                        "file": {
                            "type": "string",
                            "format": "binary"
                        }
                    },
                    "required": ["file"]
                }
            },
            responses={200: OpenApiTypes.OBJECT}
            )
    @action(
        detail=False,
        methods=["post"],
        url_path="vegetables"
    )
    def upload_vegetables(self, request):

        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "Excel file is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = bulk_upload_vegetables(file)

        return Response(
            result,
            status=status.HTTP_200_OK
        )
    
class VegetableMasterViewSet(viewsets.ModelViewSet):
    queryset = VegetableMaster.objects.all()
    serializer_class = VegetableMasterSerializer
    permission_classes = [IsSuperAdminOrReadOnly]


class SHGViewSet(viewsets.ModelViewSet):
    queryset = SHG.objects.select_related('jail').all()
    serializer_class = SHGSerializer
    permission_classes = [IsSuperAdminOrReadOnly]


class JailViewSet(viewsets.ModelViewSet):
    queryset = Jail.objects.prefetch_related('shgs').all()
    serializer_class = JailSerializer
    permission_classes = [IsSuperAdminOrReadOnly]

