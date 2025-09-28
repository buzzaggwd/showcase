from apps.services.service import DataService
from celery import shared_task


@shared_task
def service_task():
    results = DataService.save_all()
    for r in results:
        print(r)
