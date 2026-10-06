from rest_framework import serializers
from .models import Hotel, SHG, VegetableMaster


class VegetableMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = VegetableMaster
        fields = '__all__'


class SHGSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)

    class Meta:
        model = SHG

        fields = ['id', 'name', 'hotel', 'hotel_name', 'contact_person', 'is_active']


class HotelSerializer(serializers.ModelSerializer):
    shgs = SHGSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id',
            'name',
            'location',
            'is_active',
            'shgs'
        ]


class HotelBulkUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = [
            "name",
            "location",
            "is_active",
        ]


class SHGBulkUploadSerializer(serializers.ModelSerializer):

    jail = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all()
    )

    class Meta:
        model = SHG
        fields = [
            "name",
            "jail",
            "contact_person",
            "is_active",
        ]


class VegetableBulkUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = VegetableMaster
        fields = [
            "item_name",
            "unit",
            "punjabi_name",
            "category",
            "rate",
            "is_active",
        ]