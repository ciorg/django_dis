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

                if p1 == 1.001 or p1 == 'nan':
                    pass

                else:
                    for y in range(x - 1, 0, -1):
                        p2, f2 = prices[y - 1].p, prices[y - 1].f

                        if p2 == 1.001 or p2 == 'nan':
                            continue

                        else:
                            profit = abs(p1 - p2) - ((p1 * f1) + (p2 * f2))

                        if profit > high:
                            high = profit
                            dir = [prices[x - 1], prices[y - 1]]
                            dir.sort(key=lambda x: x.p)
                            p_perc = (profit/dir[0].p)*100
                            hp_data = (profit, dir[0].ex, dir[1].ex, dir[0].p, dir[1].p, p_perc)

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
        return ("{:,.2f}".format(data[0]), self.exchanges(data[1]), self.exchanges(data[2]),
                "{:,.2f}".format(data[3]), "{:,.2f}".format(data[4]), "{:,.2f}".format(data[5]))