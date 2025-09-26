from django.shortcuts import render
import requests
from apps.services.models import Service, ServiceData
from django.utils.dateformat import format as date_format
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.utils import timezone
from datetime import timedelta

def index(request):
    response = requests.get("http://127.0.0.1:8000/services/api/services/data/")
    data = response.json() if response.status_code == 200 else {}

    services = data.get("services", [])
    last_updated = data.get("last_updated")
    services_obj = Service.objects.all()

    for s in services:
        val = s.get("balance")
        try:
            s['balance'] = float(val) if val not in (None, "") else 0.0
        except (ValueError, TypeError):
            s['balance'] = 0.0

    total_spent = 0
    total_added = 0
    currency = None

    for service in services_obj:
        history_list = ServiceData.objects.filter(service_id=service.id).order_by('created_at')
        if not history_list.exists():
            continue

        currency = history_list.first().currency or currency or "—"
        prev_balance = history_list.first().balance

        for entry in history_list[1:]:
            diff = entry.balance - prev_balance
            if diff > 0:
                total_added += diff
            elif diff < 0:
                total_spent += abs(diff)
            prev_balance = entry.balance

    chart_labels = []
    chart_values = []

    for service in services_obj:
        one_month_ago = timezone.now() - timedelta(days=30)
        history_list = ServiceData.objects.filter(service_id=service.id, created_at__gte=one_month_ago).order_by("created_at")
        for h in history_list:
            if h.created_at and h.balance is not None:
                chart_labels.append(h.created_at.strftime("%Y-%m-%d"))
                chart_values.append(float(h.balance))

    min_val = min(chart_values) if chart_values else 0
    max_val = max(chart_values) if chart_values else 0

    history = {
        "total_spent": round(total_spent, 2),
        "total_added": round(total_added, 2),
        "currency": currency,
    }

    chart_data = {
        "labels": chart_labels,
        "values": chart_values,
        "min_val": min_val,
        "max_val": max_val,
    }

    return render(request, 'index.html', {
        "service_data": services,
        "history": history,
        "last_updated": last_updated,
        "chart_data": json.dumps(chart_data, cls=DjangoJSONEncoder)
    })


def widget_basic_card(request):
    response = requests.get("http://127.0.0.1:8000/services/api/services/data/")
    data = response.json() if response.status_code == 200 else {}

    services = Service.objects.all()
    services_history = []

    for service in services:
        history_list = ServiceData.objects.filter(service_id=service.id).order_by("created_at")

        if not history_list.exists():
            continue

        total_spent = 0
        total_added = 0
        currency = history_list.first().currency or "—"

        prev_balance = history_list.first().balance
        for entry in history_list[1:]:
            diff = entry.balance - prev_balance
            if diff > 0:
                total_added += diff
            elif diff < 0:
                total_spent += abs(diff)
            prev_balance = entry.balance

        services_history.append({
            "service_name": service.name,
            "total_spent": round(total_spent, 2),
            "total_added": round(total_added, 2),
            "currency": currency
        })

    history_entries = []

    for service in services:
        history_list = ServiceData.objects.filter(service_id=service.id).order_by("created_at")
        prev_balance = None
        for entry in history_list:
            if prev_balance is not None:
                diff = entry.balance - prev_balance
                if diff == 0:
                    continue
                history_entries.append({
                    "service_name": service.name,
                    "date": entry.created_at,
                    "type": "Пополнение" if diff > 0 else "Списание",
                    "amount": round(abs(diff), 2),
                    "currency": entry.currency or "—",
                })
            prev_balance = entry.balance

    last_updated = data.get("last_updated")

    return render(request, 'widget-basic-card.html', {
        "history": services_history,
        "history_entries": history_entries,
        "last_updated": last_updated
    })


def page_login(request):
    return render(request, 'page-login.html')


def farpost(request):
    return render(request, 'farpost.html')


def farpost_history(request):
    return render(request, 'farpost-history.html')


def login(request):
    return render(request, 'page-login.html')

def error(request):
    return render(request, '404.html')