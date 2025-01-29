from rest_framework import serializers
from .models import LocksmithProfile

class LocksmithProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocksmithProfile
        fields = '__all__'
