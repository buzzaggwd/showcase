from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ServiceData(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    # ОСНОВНЫЕ ФИНАНСОВЫЕ ПОЛЯ
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Sipuni, TimeWeb, Yandex Cloud, Proxy Market, ProxyLine, Dadata
    currency = models.CharField(max_length=10, default="RUB") # Sipuni, TimeWeb, Yandex Cloud
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # TimeWeb

    # ДАТЫ И СРОКИ
    subscription_end = models.DateTimeField(null=True, blank=True) # Sipuni (license_date_end), ProxyLine (date_end прокси)
    hours_left = models.IntegerField(null=True, blank=True) # TimeWeb

    # СЕРВИС-СПЕЦИФИЧНЫЕ ЛИМИТЫ
    tokens_remaining = models.IntegerField(null=True, blank=True) # Dadata (suggestions)
    proxies_count = models.IntegerField(null=True, blank=True) # Proxy Market (total), ProxyLine (count=1000)
    active_proxies_count = models.IntegerField(null=True, blank=True) # ProxyLine (results.count=4)
    hourly_cost = models.IntegerField(null=True, blank=True) # Timeweb
    monthly_cost = models.IntegerField(null=True, blank=True) # Timeweb

    # СЕРВИСНЫЕ ДАННЫЕ
    error_message = models.TextField(null=True, blank=True)
    raw_data = models.JSONField(default=dict) # Полные данные от API всех сервисов
    created_at = models.DateTimeField(auto_now_add=True)


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