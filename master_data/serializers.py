from rest_framework import serializers
from .models import Jail, SHG, VegetableMaster


class VegetableMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = VegetableMaster
        fields = '__all__'


class SHGSerializer(serializers.ModelSerializer):
    jail_name = serializers.CharField(source='jail.name', read_only=True)

    class Meta:
        model = SHG

        fields = ['id', 'name', 'jail', 'jail_name', 'contact_person', 'is_active']


class JailSerializer(serializers.ModelSerializer):
    shgs = SHGSerializer(many=True, read_only=True)

    class Meta:
        model = Jail
        fields = [
            'id',
            'name',
            'location',
            'is_active',
            'shgs'
        ]


class JailBulkUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jail
        fields = [
            "name",
            "location",
            "is_active",
        ]


class SHGBulkUploadSerializer(serializers.ModelSerializer):

    jail = serializers.PrimaryKeyRelatedField(
        queryset=Jail.objects.all()
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