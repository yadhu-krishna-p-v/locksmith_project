from rest_framework import serializers
from .models import LocksmithProfile, LocksmithService

class LocksmithProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocksmithProfile
        fields = ["business_name", "location_latitude", "location_longitude", "service_radius_km", "approved"]

class LocksmithServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = LocksmithService
        fields = ["id", "category", "category_name", "price", "car_manufacturer", "car_model", "car_year", "key_features"]
