from django.core.management.base import BaseCommand
from apps.services.parsers import parse_sipuni, parse_timeweb, parse_dadata, parse_proxy_market, parse_yandex_cloud, parse_proxyline
# from apps.services.parsers import parse_farpost
from apps.services.service import DataService

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         parse_sipuni()
#         parse_timeweb()
#         parse_dadata()
#         parse_proxy_market()
#         # parse_farpost()
#         parse_yandex_cloud()
#         parse_proxyline()

class Command(BaseCommand):
    def handle(self, *args, **options):
        results = DataService.save_all()
        for r in results:
            self.stdout.write(self.style.SUCCESS(r))