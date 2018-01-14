import requests
import json
import logging


class Exchanges(object):
    def __init__(self, coin):
        self.coin = coin
        logging.basicConfig(filename='logs/exchanges.log', level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

    def check(self, price):
        if price:
            return price

        else:
            return 1.001

    def binance(self):
        coins_dict = {"btc": "BTCUSDT",
                      "eth": "ETHUSDT",
                      "ethb": "ETHBTC"}

        url = "https://api.binance.com/api/v3/ticker/price?"

        try:
            cf = coins_dict[self.coin]
            pair = {"symbol": cf}
            data = requests.get(url, params=pair, timeout=0.5)
            jdata = json.loads(data.text)
            return self.check(float(jdata['price']))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000

    def bitfinex(self):
        coins_dict = {'btc': 'tBTCUSD',
                      'eth': 'tETHUSD',
                      'ethb': 'tETHBTC'}

        url = "https://api.bitfinex.com/v2/ticker/{}"

        # [ BID, BID_SIZE, ASK, ASK_SIZE, DAILY_CHANGE, DAILY_CHANGE_PERC, LAST_PRICE, VOLUME, HIGH, LOW ]

        try:
            url = url.format(coins_dict.get(self.coin))
            ticker_data = requests.get(url, timeout=0.5)
            jdata = json.loads(ticker_data.text)
            return self.check(float(jdata[6]))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000

    def bitstamp(self):
        coins_dict = {'btc': 'btcusd',
                      'eth': 'ethusd',
                      'ethb': 'ethbtc'}

        url = 'https://www.bitstamp.net/api/v2/ticker/{}/'

        try:
            url = url.format(coins_dict[self.coin])
            bit_r = requests.get(url, timeout=0.5)
            bit_r_json = json.loads(bit_r.text)
            return self.check(float(bit_r_json.get('last')))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000

    def coinbase(self):
        coins_dict = {'btc': 'BTC-USD',
                      'eth': 'ETH-USD',
                      'ltc': 'LTC-USD',
                      }

        url = "https://api.coinbase.com/v2/prices/{}/spot"

        try:
            cf = coins_dict[self.coin]
            url = url.format(cf)
            bit_r = requests.get(url, timeout=0.5)
            bit_r_json = json.loads(bit_r.text)

            return self.check(float(bit_r_json.get('data').get("amount")))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000

    def gemini(self):
        coins_dict = {'btc': 'btcusd',
                      'eth': 'ethusd',
                      'ethb': 'ethbtc'}

        url = "https://api.gemini.com/v1/pubticker/{}"

        try:
            cf = coins_dict[self.coin]
            url = url.format(cf)
            ticker_data = requests.get(url, timeout=0.5)
            jdata = json.loads(ticker_data.text)
            return self.check(float(jdata.get("ask")))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000

    def gdax(self):
        coins_dict = {'btc': 'BTC-USD',
                      'eth': 'ETH-USD',
                      'ethb': 'ETH-BTC'}

        url = 'https://api.gdax.com/products/{}/book'

        try:
            url = url.format(coins_dict[self.coin])
            ticker_data = requests.get(url, timeout=0.5)
            jdata = json.loads(ticker_data.text)
            return self.check(float(jdata.get('bids')[0][0]))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000

    def kraken(self):
        coins_dict = {'btc': 'XBTUSD',
                      'eth': 'ETHUSD',
                      'ltc': 'LTCUSD',
                      'ethb': 'ETHXBT'}

        url = "https://api.kraken.com/0/public/Ticker?"

        cf = coins_dict[self.coin]
        ccall = list(cf)
        ccall.insert(0, "X")
        ccall.insert(-3, "Z")
        ccall = "".join(ccall)
        pair = {"pair": cf}

        try:
            data = requests.get(url, params=pair, timeout=0.5)
            jdata = json.loads(data.text)
            return self.check(float(jdata.get('result').get(ccall).get('c')[0]))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000


if __name__ == "__main__":
    c = Exchanges("ethb")
    # print(c.binance())
    # print (c.bitfinex())
    # print(c.bitstamp())
    # print(c.coinbase())
    # print(c.gemini())
    print(c.gdax())
    # print(c.kraken())

