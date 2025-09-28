import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'showcase.settings')

# Настройки для Windows
if os.name == 'nt':
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('showcase')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')