# Use http API of Kraken to dca 100€ or so per week
import urllib.parse
from datetime import datetime
from decimal import Decimal, ROUND_DOWN

from apscheduler.schedulers.blocking import BlockingScheduler

import config

import requests
import json
import hashlib
import hmac
import base64
import time

from apscheduler_classes import add_job


class KrakenClient:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://api.kraken.com"

    def get_ticker_info(self, pair):
        response = requests.get(f"{self.base_url}/0/public/Ticker?pair={pair}")
        return response.json()

    def add_order(self, pair, type, ordertype, oflags, volume, price):
        url_path = "/0/private/AddOrder"
        data = {
            "nonce": str(int(1000 * time.time())),
            "ordertype": ordertype,
            "oflags": oflags,
            "type": type,
            "volume": volume,
            "pair": pair,
            "price": price,
        }
        headers = self._get_kraken_headers(data, url_path)
        response = requests.post(
            f"{self.base_url}{url_path}", headers=headers, data=data
        )
        return response.json()

    def get_orders(self):
        url_path = "/0/private/ClosedOrders"
        data = {"nonce": str(int(1000 * time.time())), "trades": True}
        headers = self._get_kraken_headers(data, url_path)
        response = requests.post(
            f"{self.base_url}{url_path}", headers=headers, data=data
        )
        return response.json()

    def get_account_balance(self):
        url_path = "/0/private/Balance"
        data = {"nonce": str(int(1000 * time.time()))}
        headers = self._get_kraken_headers(data, url_path)
        response = requests.post(
            f"{self.base_url}{url_path}", headers=headers, data=data
        )
        return response.json()

    def _get_kraken_headers(self, data, url_path):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data["nonce"]) + postdata).encode()
        message = url_path.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.secret_key), message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())

        headers = {"API-Key": self.api_key, "API-Sign": sigdigest.decode()}
        return headers


def main():
    print(f"Starting Buy at {datetime.now()}")
    client = KrakenClient(config.API_KEY, config.SECRET_KEY)

    bas_cur = config.BASE_CURRENCY
    bas_cur_sym = config.BASE_CURRENCY_SYMBOL
    balances = client.get_account_balance()
    base_balance = balances["result"][bas_cur]
    print(f"Current Balance: {base_balance}{bas_cur_sym}")
    for dca_pair in config.DCA:
        pair = dca_pair["pair"]
        amount_worth = dca_pair["amount_worth"]
        symbol = dca_pair["symbol"]

        print(f"Buying {amount_worth}{bas_cur_sym} worth of {symbol}")
        ticker_info = client.get_ticker_info(pair)
        # print(json.dumps(ticker_info, indent=4))

        ask_price = ticker_info["result"][pair]["b"][0]
        ask_price = Decimal(ask_price).quantize(Decimal("1.00")) - Decimal("0.5")
        print(f"Ask Price: {ask_price}€")

        # dummy_price = (ask_price / 10).quantize(Decimal("1"))
        # print(dummy_price)

        amount = (amount_worth / ask_price).quantize(Decimal("1.00000000"), ROUND_DOWN)
        print(f"Amount: {amount}{symbol}")

        # Add a buy order of 0.01 Bitcoin with Euro
        order_info = client.add_order(pair, "buy", "limit", "post", amount, ask_price)
        print(json.dumps(order_info, indent=4))
        print()


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    add_job(scheduler, main, "DCA_JOB", config.schedule)
    scheduler.start()
