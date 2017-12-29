import requests
import json


class Exchange(object):
    def __init__(self, coin):
        self.coin = coin
        self.exchange = ""

    def coin_format(self):
        position_dict = {"cb": 0,
                         "gem": 1}

        coin_dict = {'btc': ["BTC", "btcusd"],
                     'eth': ["ETH", "ethusd"],
                     'ltc': ["LTC"]}

        return coin_dict.get(self.coin)[position_dict.get(self.exchange)]


class Coinbase(Exchange):
    def __init__(self, coin):
        Exchange.__init__(self, coin)
        self.url = "https://api.coinbase.com/v2/prices/{}-USD/spot"
        self.exchange = "cb"

    def get_price(self):
        fcoin = self.coin_format()
        url = self.url.format(fcoin)
        bit_r = requests.get(url)
        bit_r_json = json.loads(bit_r.text)
        return float(bit_r_json.get('data').get("amount"))


class Gemini(Exchange):

    def __init__(self, coin):
        Exchange.__init__(self, coin)
        self.url = "https://api.gemini.com/v1/pubticker/{}"
        self.exchange = "gem"

    def get_price(self):
        fcoin = self.coin_format()
        url = self.url.format(fcoin)
        ticker_data = requests.get(url)
        jdata = json.loads(ticker_data.text)
        return float(jdata.get("ask"))

if __name__ == "__main__":
    pass