from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


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