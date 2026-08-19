from rest_framework import serializers

from .models import Demand, DemandItem
from master_data.models import Jail, SHG, VegetableMaster
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
            "confirmed_quantity"
            "price",
            "amount",
        ]

        read_only_fields = [
            "id",
            "vegetable_name",
            "amount",
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

    jail = serializers.PrimaryKeyRelatedField(
    queryset=Jail.objects.filter(
        is_active=True
    )
    shg = serializers.PrimaryKeyRelatedField(
        queryset=SHG.objects.filter(
            is_active=True
        )
    )

)
    items = DemandItemSerializer(
        many=True
    )

    jail_name = serializers.CharField(
        source="jail.name",
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
            "jail",
            "jail_name",
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
            "jail_name",
            "shg_name",
        ]

    def validate(self, attrs):

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

        jail = attrs.get("jail")
        shg = attrs.get("shg")

        if jail and shg:

            if shg.jail_id != jail.id:

                raise serializers.ValidationError({
                    "shg": (
                        "Selected SHG does not belong "
                        "to the selected Jail."
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