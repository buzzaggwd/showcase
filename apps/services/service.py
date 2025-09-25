from .models import Service, ServiceData
from .parsers import *
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

class DataService:

    @staticmethod
    def save_data_sipuni():
        service, created = Service.objects.get_or_create(
            name="Sipuni",
            defaults={
                "api_key": settings.SIPUNI_API_KEY,
                "description": "Телефония",
                "is_active": True
            }
        )

        raw_data = parse_sipuni()

        if not raw_data:
            return "Ошибка: не удалось получить данные Sipuni"

        try:
            first_response = raw_data[0]["data"]
            second_response = raw_data[1]["data"]

            license_date_end = None
            license_date_str = first_response.get("licenseDateEnd")
            
            if license_date_str:
                try:
                    license_date_end = datetime.strptime(license_date_str, "%Y.%m.%d")
                    # license_date_end = timezone.make_aware(license_date_end)
                except ValueError as e:
                    print(f"Ошибка парсинга даты: {e}")
                    license_date_end = None

            service_data = ServiceData.objects.create(
                service=service,
                balance=float(second_response.get("totalBalance", 0)),
                currency="RUB" if first_response.get("currency") == "RUR" else first_response.get("currency", "RUB"),
                subscription_end=license_date_end,
                raw_data=raw_data
            )
            
            return f"Данные Sipuni сохранены успешно! ID: {service_data.id}"

        except Exception as e:
            ServiceData.objects.create(
                service=service,
                error_message=str(e),
                raw_data={"error": str(e), "original_data": raw_data}
            )
            return f"Ошибка при сохранении Sipuni: {e}"


    @staticmethod
    def save_data_timeweb():
        service, created = Service.objects.get_or_create(
            name="TimeWeb",
            defaults={
                "api_key": settings.TIMEWEB_API_KEY,
                "description": "Хостинг",
                "is_active": True
            }
        )

        raw_data = parse_timeweb()

        if not raw_data:
            return "Ошибка: не удалось получить данные Timeweb"

        try:
            first_response = raw_data[0]["finances"]

            hours_left = first_response.get("hours_left", 0)
        
            subscription_end = None
            if hours_left and hours_left > 0:
                subscription_end = timezone.now() + timedelta(hours=hours_left)

            service_data = ServiceData.objects.create(
                service=service,
                balance=float(first_response.get("balance", 0)),
                currency=first_response.get("currency", "RUB"),
                total_paid=first_response.get("total_paid", 0),
                hours_left=first_response.get("hours_left", 0),
                subscription_end=subscription_end,
                hourly_cost=first_response.get("hourly_cost", 0),
                monthly_cost=first_response.get("monthly_cost", 0),
                raw_data=raw_data
            )
            
            return f"Данные Timeweb сохранены успешно! ID: {service_data.id}"

        except Exception as e:
            ServiceData.objects.create(
                service=service,
                error_message=str(e),
                raw_data={"error": str(e), "original_data": raw_data}
            )
            return f"Ошибка при сохранении Timeweb: {e}"


    @staticmethod
    def save_data_dadata():
        service, created = Service.objects.get_or_create(
            name="Dadata",
            defaults={
                "api_key": f"{settings.DATADATA_API_TOKEN} - {settings.DATADATA_API_SECRET}",
                "description": "API для проверки данных",
                "is_active": True
            }
        )
        
        try:
            balance, stats = parse_dadata()
            
            service_data = ServiceData.objects.create(
                service=service,
                balance=float(balance),
                currency="RUB",
                tokens_remaining=stats.get("remaining", {}).get("suggestions", 0),
                raw_data={"balance": balance, "statistics": stats}
            )
            
            return f"Данные Dadata сохранены успешно! ID: {service_data.id}"
            
        except Exception as e:
            ServiceData.objects.create(
                service=service,
                error_message=str(e),
                raw_data={'error': str(e)}
            )
            return f"Ошибка при сохранении Dadata: {e}"


    @staticmethod
    def save_data_proxy_market():
        service, created = Service.objects.get_or_create(
            name="Proxy Market",
            defaults={
                "api_key": settings.PROXY_MARKET_API_KEY,
                "description": "Прокси",
                "is_active": True
            }
        )

        raw_data = parse_proxy_market()

        if not raw_data:
            return "Ошибка: не удалось получить данные Proxy Market"

        try:
            first_response = raw_data[0]
            second_response = raw_data[1]["data"]

            service_data = ServiceData.objects.create(
                service=service,
                balance=float(first_response.get("balance", 0)),
                currency="RUB",
                proxies_count=first_response.get("proxies_count", 0),
                raw_data=raw_data
            )
            
            return f"Данные Proxy Market сохранены успешно! ID: {service_data.id}"

        except Exception as e:
            ServiceData.objects.create(
                service=service,
                error_message=str(e),
                raw_data={"error": str(e), "original_data": raw_data}
            )
            return f"Ошибка при сохранении Proxy Market: {e}"


    @staticmethod
    def save_data_yandex_cloud():
        service, created = Service.objects.get_or_create(
            name="Yandex Cloud",
            defaults={
                "api_key": f"{settings.YANDEX_CLOUD_ID} - {settings.YANDEX_CLOUD_OAUTH_TOKEN}",
                "description": "Облачные хранилища",
                "is_active": True
            }
        )

        raw_data = parse_yandex_cloud()

        if not raw_data:
            return "Ошибка: не удалось получить данные Yandex Cloud"

        try:
            first_response = raw_data[0]

            service_data = ServiceData.objects.create(
                service=service,
                balance=float(first_response.get("balance", 0)),
                currency=first_response.get("currency", "RUB"),
                raw_data=raw_data
            )
            
            return f"Данные Yandex Cloud сохранены успешно! ID: {service_data.id}"

        except Exception as e:
            ServiceData.objects.create(
                service=service,
                error_message=str(e),
                raw_data={"error": str(e), "original_data": raw_data}
            )
            return f"Ошибка при сохранении Yandex Cloud: {e}"


    @staticmethod
    def save_data_proxyline():
        service, created = Service.objects.get_or_create(
            name="ProxyLine",
            defaults={
                "api_key": settings.PROXYLINE_API_KEY,
                "description": "Прокси",
                "is_active": True
            }
        )

        raw_data = parse_proxyline()

        if not raw_data:
            return "Ошибка: не удалось получить данные Proxyline"

        try:
            first_response = raw_data[0]
            second_response = raw_data[1]
            third_response = raw_data[2]

            service_data = ServiceData.objects.create(
                service=service,
                balance=float(first_response.get("balance", 0)),
                currency="RUB",
                subscription_end=third_response["results"][0].get("date_end"),
                proxies_count=second_response.get("count", 0),
                active_proxies_count=third_response.get("count", 0),
                raw_data=raw_data
            )
            
            return f"Данные Proxyline сохранены успешно! ID: {service_data.id}"

        except Exception as e:
            ServiceData.objects.create(
                service=service,
                error_message=str(e),
                raw_data={"error": str(e), "original_data": raw_data}
            )
            return f"Ошибка при сохранении Proxyline: {e}"


    @staticmethod
    def save_all():
        results = []
        results.append(DataService.save_data_sipuni())
        results.append(DataService.save_data_timeweb())
        results.append(DataService.save_data_dadata())
        results.append(DataService.save_data_proxy_market())
        results.append(DataService.save_data_yandex_cloud())
        results.append(DataService.save_data_proxyline())
        return results


    @staticmethod
    def get_latest_data():
        service_data =[]
        for service in Service.objects.all():
            latest_data = ServiceData.objects.filter(
                service=service
            ).order_by('-created_at').first()

            if latest_data:
                service_data.append({
                    "name":service.name,
                    "type":service.type,
                    "price":latest_data.price,
                    "created_at":latest_data.created_at
                })