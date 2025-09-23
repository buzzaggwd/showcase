import requests
from dadata import Dadata
from django.conf import settings

def parse_sipuni():
    pass


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


if __name__ == "__main__":
    parse_timeweb()
    parse_dadata()
    parse_proxy_market()
    parse_yandex_cloud()
    parse_proxyline()