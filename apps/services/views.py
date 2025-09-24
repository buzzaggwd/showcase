from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Service, ServiceData
from .serializers import ServiceSerializer, ServiceDataSerializer
from .service import DataService


# -----------------------API--------------------------
class GetServiceInfoView(APIView):
    def get(self, request):
        service_ids = request.query_params.get("services")
        queryset = Service.objects.all()

        if service_ids:
            try:
                ids = [int(x) for x in service_ids.split(",") if x.strip().isdigit()]
                queryset = queryset.filter(id__in=ids)
            except ValueError:
                return Response({"error": "Неверный формат параметра 'services'. Используйте ?services=1,2,3"}, status=400)

        serializer = ServiceSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer.data)


class GetServiceDataInfoView(APIView):
    def get(self, request):
        service_ids = request.query_params.get("services")
        queryset = ServiceData.objects.all()

        if service_ids:
            try:
                ids = [int(x) for x in service_ids.split(",") if x.strip().isdigit()]
                queryset = queryset.filter(service_id__in=ids)
            except ValueError:
                return Response({"error": "Неверный формат параметра 'services'. Используйте ?services=1,2,3"}, status=400)

        latest_ids = []
        for service_id in queryset.values_list('service_id', flat=True).distinct():
            latest = queryset.filter(service_id=service_id).order_by('-created_at').first()
            if latest:
                latest_ids.append(latest.id)
        
        queryset = queryset.filter(id__in=latest_ids)

        serializer = ServiceDataSerializer(
            instance=queryset,
            many=True,
        )

        filtered_data = []
        for item in serializer.data:
            filtered_item = {k: v for k, v in item.items() if v is not None}
            filtered_data.append(filtered_item)

        return Response(filtered_data)