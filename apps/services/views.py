from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Service, ServiceData
from .serializers import ServiceSerializer, ServiceDataSerializer
from .service import DataService

# ------------------------DB--------------------------
# class SaveSipuniDataView(APIView):
#     def get(self, request):
#         result = DataService.save_data_sipuni()
#         return Response({"message": result})


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

        serializer = ServiceDataSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer.data)