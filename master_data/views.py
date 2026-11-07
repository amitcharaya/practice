from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Hotel, SHG, VegetableMaster
from .serializers import HotelSerializer, SHGSerializer, VegetableMasterSerializer
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
import pandas as pd
from rest_framework import generics

class VegetableBulkUploadView(APIView):
    """
    Super Admin uses this endpoint to upload an Excel file 
    containing master vegetable lists.
    """
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
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
    def post(self, request):
        if request.user.role != "SA":
            return Response(
                {"error": "Only Super Admin can perform bulk uploads."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        file = request.FILES.get('file')
        if not file or not file.name.endswith(('.xls', '.xlsx')):
            return Response(
                {"error": "Please provide a valid Excel file (.xls or .xlsx)."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse spreadsheet with pandas
        df = pd.read_excel(file)
        bulk_instances = []
        
        for _, row in df.iterrows():
            item_name = row.get('item_name')
            if item_name and not VegetableMaster.objects.filter(item_name=item_name).exists():
                bulk_instances.append(VegetableMaster(
                    item_name=item_name,
                    unit=row.get('unit', 'kg'),
                    category=row.get('category', 'Vegetables'),
                    rate=row.get('rate', 0),
                    punjabi_name=row.get('punjabi_name'),
                    is_active=row.get('is_active')
                ))
        
        VegetableMaster.objects.bulk_create(bulk_instances)
        return Response(
            {"message": f"Successfully imported {len(bulk_instances)} items."}, 
            status=status.HTTP_201_CREATED
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



    


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.prefetch_related('shgs').all()
    serializer_class = HotelSerializer
    permission_classes = [IsSuperAdminOrReadOnly]

class HotelListCreateView(generics.ListAPIView):
    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]

class SHGViewSet(viewsets.ModelViewSet):
    """
    Provides complete CRUD for SHG vendor groups with multi-tenant filtering.
    """
    queryset = SHG.objects.all()
    serializer_class = SHGSerializer
    permission_classes = [IsSuperAdminOrReadOnly]

    def get_queryset(self):
        """Enforce multi-tenant data isolation dynamically based on the requesting user."""
        user = self.request.user
        
        # If the user is a Hotel User (HU) and is assigned to a hotel, 
        # restrict the query to only their hotel's SHGs.
        if user.role == 'HU' and user.hotel:
            return SHG.objects.filter(hotel=user.hotel)
            
        # Super Admins see everything
        return SHG.objects.all()

    @action(detail=True, methods=['post'])
    def verify_vendor(self, request, pk=None):
        """Custom action: Admin can verify a vendor's cooperative license"""
        shg = self.get_object()
        shg.is_verified = True
        shg.save()
        return Response({"message": f"SHG {shg.name} has been verified successfully."})

