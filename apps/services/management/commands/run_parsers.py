from django.core.management.base import BaseCommand
from apps.services.parsers import parse_timeweb, parse_dadata, parse_proxy_market, parse_farpost, parse_yandex_cloud, parse_proxyline

class Command(BaseCommand):
    help = 'Run parsers for various services'

    def handle(self, *args, **options):
        parse_timeweb()
        parse_dadata()
        parse_proxy_market()
        parse_farpost()
        parse_yandex_cloud()
        parse_proxyline()