from django.db import models

SERVICE_TYPES = [
        ("sipuni", "Sipuni"),
        ("dadata", "Dadata"),
        ("proxy_market", "Proxy Market"),
        ("timeweb", "TimeWeb"),
        ("farpost", "Farpost"),
        ("yandex_cloud", "Yandex Cloud"),
        ("proxyline", "ProxyLine"),
    ]

class Service(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=SERVICE_TYPES)
    api_key = models.CharField(max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    duration = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ServiceData(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Sipuni, TimeWeb, Yandex Cloud, Proxy Market, ProxyLine, Dadata
    currency = models.CharField(max_length=10, default="RUB") # Sipuni, TimeWeb, Yandex Cloud
    subscription_end = models.DateTimeField(null=True, blank=True) # Sipuni (license_date_end), ProxyLine (date_end прокси)
    tokens_remaining = models.IntegerField(null=True, blank=True) # Dadata (suggestions)
    proxies_count = models.IntegerField(null=True, blank=True) # Proxy Market (total), ProxyLine (count=1000)
    hours_left = models.IntegerField(null=True, blank=True) # TimeWeb (hours_left)
    active_proxies_count = models.IntegerField(null=True, blank=True) # ProxyLine (results.count=4)
    companies_count = models.IntegerField(null=True, blank=True) # Farpost (общее число компаний)
    license_date_end = models.DateTimeField(null=True, blank=True)  # Sipuni (license_date_end)
    user_name = models.CharField(max_length=255, null=True, blank=True)  # Sipuni (name)
    phone_number = models.CharField(max_length=20, null=True, blank=True)  # Sipuni (phone)
    raw_data = models.JSONField(default=dict) # Полные данные от API всех сервисов
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class FarpostCompany(models.Model):
#     service_data = models.ForeignKey(ServiceData, on_delete=models.CASCADE, related_name='farpost_companies')
#     company_name = models.CharField(max_length=255)
#     ads_count = models.IntegerField(default=0)
#     ads_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     balance = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

class ServiceDataHistory(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)