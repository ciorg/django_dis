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
            return 0.000

    def binance(self):
        coins_dict = {"btc": "BTCUSDT",
                      "eth": "ETHUSDT",
                      "ethb": "ETHBTC",
                      "ltc": 'LTCUSDT',
                      'ltcb': 'LTCBTC',
                      'bchb': 'BCCBTC',
                      'xmrb': 'XMRBTC',
                      'xrpb': 'XRPBTC'
                     }

        url = "https://api.binance.com/api/v3/ticker/price?"

        try:
            cf = coins_dict[self.coin]
            pair = {"symbol": cf}
            data = requests.get(url, params=pair, timeout=5)
            jdata = json.loads(data.text)
            # print(jdata)
            return self.check(float(jdata['price']))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000

    def bitfinex(self):
        coins_dict = {'btc': 'tBTCUSD',
                      'eth': 'tETHUSD',
                      'ethb': 'tETHBTC',
                      'ltc': 'tLTCUSD',
                      'ltcb': 'tLTCBTC',
                      'bchb': 'tBCHBTC',
                      'xmrb': 'tXMRBTC',
                      'xrpb': 'tXRPBTC'}

        url = "https://api.bitfinex.com/v2/ticker/{}"

        # [ BID, BID_SIZE, ASK, ASK_SIZE, DAILY_CHANGE, DAILY_CHANGE_PERC, LAST_PRICE, VOLUME, HIGH, LOW ]

        try:
            url = url.format(coins_dict.get(self.coin))
            ticker_data = requests.get(url, timeout=5)
            jdata = json.loads(ticker_data.text)
            return self.check(float(jdata[6]))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000

    def bitstamp(self):
        coins_dict = {'btc': 'btcusd',
                      'eth': 'ethusd',
                      'ethb': 'ethbtc',
                      'ltc': 'ltcusd',
                      'ltcb': 'ltcbtc',
                      'bchb': 'bchbtc',
                      'xrpb': 'xrpbtc'}

        url = 'https://www.bitstamp.net/api/v2/ticker/{}/'

        try:
            url = url.format(coins_dict[self.coin])
            bit_r = requests.get(url, timeout=5)
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
            bit_r = requests.get(url, timeout=5)
            bit_r_json = json.loads(bit_r.text)

            return self.check(float(bit_r_json.get('data').get("amount")))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000

    def gemini(self):
        coins_dict = {'btc': 'btcusd',
                      'eth': 'ethusd',
                      'ethb': 'ethbtc',
                      'ltc': 'ltcusd',
                      }

        url = "https://api.gemini.com/v1/pubticker/{}"

        try:
            cf = coins_dict[self.coin]
            url = url.format(cf)
            ticker_data = requests.get(url, timeout=5)
            jdata = json.loads(ticker_data.text)
            return self.check(float(jdata.get("ask")))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000

    def gdax(self):
        coins_dict = {'btc': 'BTC-USD',
                      'eth': 'ETH-USD',
                      'ethb': 'ETH-BTC',
                      'ltc': 'LTC-USD',
                      'ltcb': 'LTC-BTC',
                      }

        url = 'https://api.gdax.com/products/{}/ticker'

        try:
            url = url.format(coins_dict[self.coin])
            ticker_data = requests.get(url, timeout=5)
            jdata = json.loads(ticker_data.text)
            return self.check(float(jdata.get('price')))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000

    def kraken(self):
        coins_dict = {'btc': ('XBTUSD', 'XBTUSD'),
                      'eth': ('ETHUSD', 'XETHZUSD'),
                      'ltc': ('LTCUSD', 'XLTCZUSD'),
                      'ethb': ('ETHXBT', 'XETHXXBT'),
                      'ltcb': ('LTCXBT', 'XLTCXXBT'),
                      'bchb': ('BCHXBT', 'BCHXBT'),
                      'xmrb': ('XMRXBT','XXMRXXBT'),
                      'xrpb': ('XRPXBT','XXRPXXBT')}

        url = "https://api.kraken.com/0/public/Ticker?"

        cf_d = coins_dict[self.coin]
        pair = {"pair": cf_d[0]}

        try:
            data = requests.get(url, params=pair, timeout=5.0)
            jdata = json.loads(data.text)
            return self.check(float(jdata.get('result').get(cf_d[1]).get('c')[0]))

        except Exception as e:
            logging.exception("{}".format(e))
            return 0.000


if __name__ == "__main__":
    c = Exchanges("bch")
    print("Binance: {}".format(c.binance()))
    print ("Bitfinex: {}".format(c.bitfinex()))
    print("Bitstamp: {}".format(c.bitstamp()))
    print("Coinbase:{}".format(c.coinbase()))
    print("Gemini: {}".format(c.gemini()))
    print("GDAX: {}".format(c.gdax()))
    print("Kraken: {}".format(c.kraken()))


