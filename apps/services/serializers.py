from rest_framework import serializers
from .models import Service, ServiceData

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        # fields = ["id", "name", "is_active", "description", "created_at"]

class ServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceData
        fields = "__all__"