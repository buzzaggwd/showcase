from django.shortcuts import render
import requests

def index(request):
    response = requests.get("http://127.0.0.1:8000/services/api/services/data/")
    data = response.json() if response.status_code == 200 else {}

    response_history = requests.get("http://127.0.0.1:8000/services/api/services/history/")
    data_history = response_history.json() if response_history.status_code == 200 else {}

    services = data.get("services", [])
    last_updated = data.get("last_updated")

    for s in services:
        val = s.get("balance")
        try:
            s['balance'] = float(val) if val not in (None, "") else 0.0
        except (ValueError, TypeError):
            s['balance'] = 0.0

    total_spent = 0
    currency = None

    for service in data_history["services"]:
        balances = [h["balance"] for h in service["history"] if h["balance"] is not None]
        if balances:
            start_balance = balances[0]
            min_balance = min(balances)
            spent = start_balance - min_balance if start_balance > min_balance else 0
            total_spent += spent
            if not currency:
                currency = service["history"][0]["currency"]

    history = {
        "total_paid": round(total_spent, 2),
        "currency": currency or "—",
    }

    return render(request, 'index.html', {
        "service_data": services,
        "history": history,
        "last_updated": last_updated
    })

def widget_basic_card(request):
    return render(request, 'widget-basic-card.html')

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