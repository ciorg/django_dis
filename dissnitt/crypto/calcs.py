from collections import namedtuple


class CalcClass(object):
    def __init__(self):
        pass

    def get_profit(self, prices):

        high = -10000
        hp_data = tuple()
        for x in range(len(prices), 0, -1):
            if x >= 2:
                p1, f1 = prices[x - 1].p, prices[x - 1].f

                if p1 == 0 or p1 is None:
                    pass

                else:
                    for y in range(x - 1, 0, -1):
                        p2, f2 = prices[y - 1].p, prices[y - 1].f

                        profit = abs(p1 - p2) - ((p1 * f1) + (p2 * f2))

                        if profit > high:
                            high = profit
                            dir = [prices[x - 1], prices[y - 1]]
                            dir.sort(key=lambda x: x.p)
                            hp_data = (profit, "{}->{}".format(dir[0].ex, dir[1].ex))

            else:
                pass

        return hp_data

    def exchanges(self, ex):

        ex_dict = {'cb': 'Coinbase',
                   'gem': 'Gemini',
                   'kr': 'Kraken',
                   'bi': 'Binance',
                   'bf': 'Bitfinex',
                   'bs': 'Bitstamp',
                   'gd': 'GDAX'
                   }

        return ex_dict.get(ex)

    def price_percentage(self, prices, dir):
        p1, p2 = 0, 0

        for p in prices:
            if dir[0] == p.ex:
                p1 = float(p.p)

            if dir[1] == p.ex:
                p2 = float(p.p)

        dif = abs(p1 - p2)
        return dif/p1

    def views_data(self, last_entry):
        pdata = namedtuple('pdata', 'ex, p, f')

        prices = (pdata("cb", float(last_entry.coinbase_price), 0.0149),
                  pdata("gem", float(last_entry.gemini_price), 0.0025),
                  pdata("kr", float(last_entry.kraken_price), 0.0026),
                  pdata('bi', float(last_entry.binance_price), 0.001),
                  pdata('bf', float(last_entry.bitfinex_price), 0.002),
                  pdata('bs', float(last_entry.bitstamp_price), 0.0025),
                  pdata('gd', float(last_entry.gdax_price), 0.0025))

        data = self.get_profit(prices)

        dir = data[1]
        dir = dir.split("->")

        p_dif = self.price_percentage(prices, dir)

        vdir = "{} -> {}".format(self.exchanges("".join(dir[0])), self.exchanges("".join(dir[1])))
        return data[0], vdir, p_dif * 100