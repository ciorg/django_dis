import requests
import json


class Exchanges(object):
    def __init__(self, coin):
        self.coin = coin

    def binance(self):
        coins_dict = {"btc": "BTCUSDT"}
        url = "https://api.binance.com/api/v3/ticker/price?"

        try:
            cf = coins_dict[self.coin]
            pair = {"symbol": cf}
            data = requests.get(url, params=pair)
            jdata = json.loads(data.text)
            return float(jdata['price'])

        except KeyError:
            print("No coin on this exchange")

    def bitfinex(self):
        coins_dict = {'btc': 'tBTCUSD'}
        url = "https://api.bitfinex.com/v2/ticker/{}"

        # [ BID, BID_SIZE, ASK, ASK_SIZE, DAILY_CHANGE, DAILY_CHANGE_PERC, LAST_PRICE, VOLUME, HIGH, LOW ]

        try:
            url = url.format(coins_dict.get(self.coin))
            ticker_data = requests.get(url)
            jdata = json.loads(ticker_data.text)
            return float(jdata[6])

        except:
            print("No coin on this exchange")

    def bitstamp(self):
        coins_dict = {'btc': 'btcusd'}
        url = 'https://www.bitstamp.net/api/v2/ticker/{}/'

        try:
            url = url.format(coins_dict[self.coin])
            bit_r = requests.get(url)
            bit_r_json = json.loads(bit_r.text)
            return float(bit_r_json.get('last'))

        except:
            print("No coin on this exchange")

    def coinbase(self):
        coins_dict = {'btc': 'BTC',
                      'eth': 'ETH',
                      'ltc': 'LTC'}

        url = "https://api.coinbase.com/v2/prices/{}-USD/spot"

        try:
            cf = coins_dict[self.coin]
            url = url.format(cf)
            bit_r = requests.get(url)
            bit_r_json = json.loads(bit_r.text)
            return float(bit_r_json.get('data').get("amount"))

        except KeyError:
            print("No coin on this exchange")

    def gemini(self):
        coins_dict = {'btc': 'btcusd',
                      'eth': 'ethusd'}

        url = "https://api.gemini.com/v1/pubticker/{}"
        try:
            cf = coins_dict[self.coin]
            url = url.format(cf)
            ticker_data = requests.get(url)
            jdata = json.loads(ticker_data.text)
            return float(jdata.get("ask"))

        except KeyError:
            print("No coin on this exchange")

    def gdax(self):
        coins_dict = {'btc': 'BTC-USD'}

        url = 'https://api.gdax.com/products/{}/book'

        try:
            url = url.format(coins_dict[self.coin])
            ticker_data = requests.get(url)
            jdata = json.loads(ticker_data.text)
            return float(jdata.get('bids')[0][0])

        except KeyError:
            print("No coin on this exchange")

    def kraken(self):
        coins_dict = {'btc': 'XBTUSD',
                      'eth': 'ETHUSD',
                      'ltc': 'LTCUSD'}

        url = "https://api.kraken.com/0/public/Ticker?"

        try:
            cf = coins_dict[self.coin]
            ccall = list(cf)
            ccall.insert(0, "X")
            ccall.insert(-3, "Z")
            ccall = "".join(ccall)

            pair = {"pair": cf}
            data = requests.get(url, params=pair)
            jdata = json.loads(data.text)
            return float(jdata.get('result').get(ccall).get('c')[0])

        except KeyError:
            print("No coin on this exchange")


if __name__ == "__main__":
    c = Exchanges("btc")
    print(c.bitstamp())
