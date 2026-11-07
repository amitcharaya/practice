from rest_framework import serializers
from django.utils import timezone
from .models import Demand, DemandItem,Invoice
from master_data.models import Hotel, SHG, VegetableMaster
from django.db import transaction



#Now create the DemandItemSerializer.
class DemandItemSerializer(serializers.ModelSerializer):

    vegetable = serializers.PrimaryKeyRelatedField(
        queryset=VegetableMaster.objects.filter(
            is_active=True
        )
    )

    vegetable_name = serializers.CharField(
        source="vegetable.item_name",
        read_only=True
    )

    class Meta:
        model = DemandItem

        fields = [
            "id",
            "vegetable",
            "vegetable_name",
            "quantity",
            "confirmed_quantity",
            "price",
            
        ]

        read_only_fields = [
            "id",
            "vegetable_name",
            
        ]
    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )

        return value
    def validate_price(self, value):

        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Unit rate cannot be negative."
            )

        return value

class DemandSerializer(serializers.ModelSerializer):

    hotel = serializers.PrimaryKeyRelatedField(
    queryset= Hotel.objects.filter(
        is_active=True
    ))
    shg = serializers.PrimaryKeyRelatedField(
        queryset=SHG.objects.filter(
            is_active=True
        )
    )
    
    items = DemandItemSerializer(
        many=True
    )

    hotel_name = serializers.CharField(
        source="hotel.name",
        read_only=True
    )

    shg_name = serializers.CharField(
        source="shg.name",
        read_only=True
    )

    created_by_name = serializers.CharField(
        source="created_by.username",
        read_only=True
    )

    class Meta:

        model = Demand

        fields = [
            "id",
            "hotel",
            "hotel_name",
            "shg",
            "shg_name",
            "created_by",
            "created_by_name",
            "target_date",
            "status",
            "items",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_by_name",
            "status",
            "created_at",
            "updated_at",
            "hotel_name",
            "shg_name",
        ]

    def validate(self, attrs):
        """
        Object-level validation to enforce cross-field business logic.
        """
        target_date = attrs.get('target_date')
        
        # Ensure the date is in the future
        if target_date and target_date <= timezone.now().date():
            # Passing a dictionary to ValidationError assigns the error 
            # to the specific field in the JSON response payload.
            raise serializers.ValidationError({
                "target_date": "Target delivery date must be at least one day in the future."
            })
            

        items = attrs.get("items", [])

        if not items:

            raise serializers.ValidationError({
                "items": (
                    "At least one vegetable item "
                    "is required."
                )
            })

        vegetable_ids = [
            item["vegetable"].id
            for item in items
        ]

        if len(vegetable_ids) != len(
            set(vegetable_ids)
        ):

            raise serializers.ValidationError({
                "items": (
                    "The same vegetable cannot "
                    "be added more than once."
                )
            })

        hotel = attrs.get("hotel")
        shg = attrs.get("shg")

        if hotel and shg:

            if shg.hotel_id != hotel.id:

                raise serializers.ValidationError({
                    "shg": (
                        "Selected SHG does not belong "
                        "to the selected Hotel."
                    )
                })

        return attrs

    def validate_target_date(self, value):

        if value < timezone.localdate():

            raise serializers.ValidationError(
                "Target date cannot be in the past."
            )

        return value

    

    def create(self, validated_data):

        items_data = validated_data.pop(
            "items",
            []
        )
        with transaction.atomic():
            demand = Demand.objects.create(
                **validated_data
            )

            for item_data in items_data:

                DemandItem.objects.create(
                    demand=demand,
                    **item_data
                )

        return demand



class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'order', 'shg_invoice_file', 'shg_amount', 'status']

    def validate_shg_invoice_file(self, value):
        """
        Enforce strict validation on the uploaded invoice document.
        The 'value' parameter is an instance of Django's UploadedFile.
        """
        # 1. Enforce a 5MB File Size Limit (5 * 1024 * 1024 bytes)
        max_file_size = 5242880  
        if value.size > max_file_size:
            raise serializers.ValidationError("Invoice file size cannot exceed 5MB.")

        # 2. Enforce File Extension
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF documents are accepted for invoices.")
            
        # 3. Enforce MIME Content Type (Secondary Security Check)
        if value.content_type != 'application/pdf':
            raise serializers.ValidationError("Invalid file format. The file content must be a PDF.")

        return value


    def validate(self, attrs):
# We use self.instance to check if we are updating an existing record
        if self.instance:
            current_status = self.instance.status
            new_status = attrs.get('status', current_status)

            # Prevent illegal state transitions
        if current_status == 'SUBMITTED' and new_status not in ['VERIFIED_HU', 'REJECTED']:
                raise serializers.ValidationError({
                "status": f"Illegal transition. Cannot move from {current_status} to {new_status}."
                })
                
        if current_status == 'VERIFIED_HU' and new_status not in ['APPROVED_HA', 'REJECTED']:
                raise serializers.ValidationError({
                "status": "A verified invoice can only transition to Approved or Rejected."
                })
                
                # If the status is moving to APPROVED, enforce that amount is finalized
        if new_status == 'APPROVED_HA' and not attrs.get('shg_amount') and not self.instance.shg_amount:
                raise serializers.ValidationError({
                    "shg_amount": "Financial amount must be finalized before approval."
                })
                
        return attrs
