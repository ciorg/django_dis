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

                if p1 == 0.000 or p1 == 'nan':

                    pass

                else:
                    for y in range(x - 1, 0, -1):
                        p2, f2 = prices[y - 1].p, prices[y - 1].f

                        if p2 == 0.000 or p2 == 'nan':
                            continue

                        else:
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

    def arbit_data(self, prices, dir):
        d_dict = {}

        for i in prices:
            d_dict[i.ex] = i.p

        p1 = d_dict.get(dir[0])
        p2 = d_dict.get(dir[1])

        return p1, p2

    def views_data(self, last_entry):
        pdata = namedtuple('pdata', 'ex, p, f')
        prices = []

        exchanges_tuple = (("cb", 'coinbase_price', 0.0149),
                           ("gem", 'gemini_price', 0.0025),
                           ("kr", 'kraken_price', 0.0026),
                           ('bi', 'binance_price', 0.001),
                           ('bf', 'bitfinex_price', 0.002),
                           ('bs', 'bitstamp_price', 0.0025),
                           ('gd', 'gdax_price', 0.0025))

        for ex in exchanges_tuple:

            try:
                price = eval("last_entry.{}".format(ex[1]))
                pd = pdata(ex[0], float(price), ex[2])
                prices.append(pd)

            except AttributeError:
                pass

        data = self.get_profit(prices)
        dir = data[1].split("->")
        ps = self.arbit_data(prices, dir)
        p_perc = (data[0]/ps[0])*100

        return (data[0], self.exchanges(dir[0]), self.exchanges(dir[1]),
                ps[0], ps[1], "{:,.2f}".format(p_perc))