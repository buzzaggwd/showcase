import requests
from dadata import Dadata
from django.conf import settings
import csv
from io import StringIO
from bs4 import BeautifulSoup
import re
import time
import random


def parse_sipuni():
    start_urls = [
        "https://apilk.sipuni.com/api/ver2/user/summary",
        # "https://apilk.sipuni.com/api/ver2/operation/list",
        "https://apilk.sipuni.com/api/ver2/info/getBalanceInfo"
    ]
    api_key = settings.SIPUNI_API_KEY
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    responses = {}
    for url in start_urls:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # print(f"[SIPUNI] {data}")
            responses[url] = data
        else:
            print(f"[SIPUNI] Ошибка: {response.status_code} - {response.text}")
            responses[url] = None
    print(f"[SIPUNI] {[response for response in responses.values()]}")


def parse_timeweb():
    start_urls = [
        "https://api.timeweb.cloud/api/v1/account/finances"
    ]
    api_key = settings.TIMEWEB_API_KEY
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    responses = {}
    for url in start_urls:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # print(f"[TIMEWEB] {data}")
            responses[url] = data
        else:
            print(f"[TIMEWEB] Ошибка: {response.status_code} - {response.text}")
            responses[url] = None
    print(f"[TIMEWEB] {[response for response in responses.values()]}")


def parse_dadata():
    dadata_token = settings.DATADATA_API_TOKEN
    dadata_secret = settings.DATADATA_API_SECRET
    dadata = Dadata(dadata_token, dadata_secret)

    balance = dadata.get_balance()
    stats = dadata.get_daily_stats()
    print(f"[DADATA] {balance} {stats}")


def parse_proxy_market():
    start_urls = [ 
        "https://virtserver.swaggerhub.com/proxy.market-api/Proxy.Market/1.1/dev-api/balance/",
        "https://virtserver.swaggerhub.com/proxy.market-api/Proxy.Market/1.1/dev-api/v2/packages/"
    ]
    api_key = settings.PROXY_MARKET_API_KEY
    headers = {
        # "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    responses = {}
    for url in start_urls:
        url = f"{url}{api_key}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # print(f"[PROXY_MARKET] {data}")
            responses[url] = data
        else:
            print(f"[PROXY_MARKET] Ошибка: {response.status_code} - {response.text}")
            responses[url] = None
    print(f"[PROXY_MARKET] {[response for response in responses.values()]}")


# def parse_farpost():
#     spreadsheet_id = settings.FARPOST_SPREADSHEET_ID
#     url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid=0'
#     url_farpost = "https://www.farpost.ru/personal/actual/bulletins"
#     r = requests.get(url)
#     r.raise_for_status()

#     reader = csv.reader(StringIO(r.text))
#     rows = list(reader)

#     if not rows:
#         raise ValueError("Таблица пустая")

#     keys = rows[0]
#     data = []

#     for row in rows[1:]:
#         entry = dict(zip(keys, row))
#         data.append(entry)

#     for item in data:
#         boobs_value = item["Boobs"]
#         name = item['               ']
#         cookies = {"boobs": boobs_value}
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
#         }

#         response = requests.get(url_farpost, cookies=cookies, headers=headers)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")
#         stick_items = soup.find_all("a", class_="service-card-head service-card-head_style_mini")

#         total_count = 0
#         total_price = 0

#         for item in stick_items:
#             if "Приклеено" in item.text:
#                 total_count += 1
#                 price_str = item.find("div")["data-writeoff"] if item.find("div") and item.find("div").has_attr("data-writeoff") else None
#                 if price_str:
#                     total_price += int(price_str)

#         # print(f"Количество объектов с приклеено: {total_count}")
#         # print(f"Общая сумма: {total_price} ₽")

#         balance_elem = soup.find("div", class_="personal-balance-info__balance")
#         if balance_elem:
#             balance_text = balance_elem.get_text(strip=True)
#             balance_number = int(re.sub(r"[^\d]", "", balance_text))
#         else:
#             print("Баланс не найден")
#             balance_number=None

#         print(f"[FARPOST] Компания {name}. Количество объявлений {total_count} на общую сумму {total_price}. Баланс: {balance_number}")
#         delay = random.uniform(2, 7)
#         # print(f"Ждeм {delay:.2f} секунд...")
#         time.sleep(delay)


def get_iam_token(oauth_token):
    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    data = {"yandexPassportOauthToken": oauth_token}
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get("iamToken")
    else:
        raise Exception(f"Ошибка получения IAM токена: {response.text}")

def parse_yandex_cloud():
    start_urls = [
        "https://billing.api.cloud.yandex.net/billing/v1/billingAccounts/",
    ]
    id = settings.YANDEX_CLOUD_ID
    oauth_token = settings.YANDEX_CLOUD_OAUTH_TOKEN

    iam_token = get_iam_token(oauth_token)
    if not iam_token:
        print("IAM токен не доступен")
        return

    responses = {}
    for url in start_urls:
        url = f"{url}{id}"
        headers = {
            "Authorization": f"Bearer {iam_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # print(f"[YANDEX_CLOUD] {data}")
            responses[url] = data
        else:
            print(f"[YANDEX_CLOUD] Ошибка: {response.status_code} - {response.text}")
            responses[url] = None
    print(f"[YANDEX_CLOUD] {[response for response in responses.values()]}")


def parse_proxyline():
    start_urls = [
        "https://panel.proxyline.net/api/balance/?api_key={api_key}",
        "https://panel.proxyline.net/api/ips-count/?api_key={api_key}&ip_version=4&type=dedicated&country=ru",
        "https://panel.proxyline.net/api/proxies/?api_key={api_key}",
        "https://panel.proxyline.net/api/orders/?api_key={api_key}"
    ]
    api_key = settings.PROXYLINE_API_KEY
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    responses = {}
    for url in start_urls:
        url = url.format(api_key=api_key)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # print(f"[PROXYLINE] {data}")
            responses[url] = data
        else:
            print(f"[PROXYLINE] Ошибка: {response.status_code} - {response.text}")
            responses[url] = None
    print(f"[PROXYLINE] {[response for response in responses.values()]}")

