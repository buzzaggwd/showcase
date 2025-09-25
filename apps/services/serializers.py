from rest_framework import serializers
from .models import Service, ServiceData

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        # fields = "__all__"
        exclude = ("api_key",)


class ServiceDataSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)
    class Meta:
        model = ServiceData
        # fields = "__all__"
        exclude = ("raw_data", "hours_left",)