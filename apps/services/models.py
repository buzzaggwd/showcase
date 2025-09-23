from django.db import models

SERVICE_TYPES = [
        ("dadata", "Dadata"),
        ("proxy_market", "Proxy Market"),
        ("timeweb", "TimeWeb"),
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
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default="RUB")
    subscription_end = models.DateTimeField(null=True, blank=True)
    tokens_remaining = models.IntegerField(null=True, blank=True)
    proxies_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ServiceDataHistory(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)