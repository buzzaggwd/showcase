from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Service, ServiceData
from .serializers import ServiceSerializer, ServiceDataSerializer
from .service import DataService
from django.utils import timezone
from datetime import datetime, timedelta


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
                queryset = queryset.filter(service_id__in=ids).order_by("service_id")
            except ValueError:
                return Response({"error": "Неверный формат параметра 'services'. Используйте ?services=1,2,3"}, status=400)

        latest_ids = []
        for service_id in queryset.values_list("service_id", flat=True).distinct():
            latest = queryset.filter(service_id=service_id).order_by("-created_at").first()
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


class GetServiceDataHistoryInfoView(APIView):
    def get(self, request):        
        period = request.query_params.get("period", "month")
        service_ids = request.query_params.get("services", "")
        start_date_str = request.query_params.get("start_date", "")
        end_date_str = request.query_params.get("end_date", "")

        today = timezone.now().date()
        if period == "month":
            start_date = today.replace(day=1)
        else: 
            start_date = today.replace(month=1, day=1)

        if not start_date_str or not end_date_str:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
        else:
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response({"error": "Неверный формат даты. Используйте YYYY-MM-DD"}, status=400)

        queryset = ServiceData.objects.filter(created_at__date__range=[start_date, end_date]).order_by('service_id', 'created_at')
        
        if service_ids:
            try:
                ids = [int(x) for x in service_ids.split(",") if x.strip().isdigit()]
                queryset = queryset.filter(service_id__in=ids)
            except ValueError:
                return Response({"error": "Неверный формат параметра 'services'. Используйте ?services=1,2,3"}, status=400)

        result = {}
        for data in queryset:
            service_id = data.service_id
            if service_id not in result:
                try:
                    service = Service.objects.get(id=service_id)
                    result[service_id] = {
                        "service_id": service_id,
                        "service_name": service.name,
                        "history": []
                    }
                except Exception:
                    continue
            
            result[service_id]["history"].append({
                "date": data.created_at.strftime("%Y-%m-%d %H:%M"),
                "balance": float(data.balance) if data.balance else 0,
                "currency": data.currency
            })

        services_list = list(result.values())
        
        return Response({
            "period": {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
            },
            "services": services_list
        })