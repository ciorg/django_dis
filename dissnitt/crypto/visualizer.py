import sqlite3
from datetime import datetime
from collections import namedtuple
from .calcs import CalcClass

from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import row, column
from bokeh.models import HoverTool
from bokeh.embed import components


class GraphClass(object):

    def __init__(self, table):
        self.db = "db.sqlite3"
        self.table = table

    def db_search(self, search):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute(search)
        data = c.fetchall()
        mdata = [x[0] for x in c.description]
        conn.close()
        return data, mdata

    def get_data(self, tf):
        cprice_dict = {'bitcoin': 'gemini_price, coinbase_price, binance_price, bitfinex_price,'
                                  'bitstamp_price, gdax_price, kraken_price',

                       'etherium': 'gemini_price, coinbase_price, binance_price, bitfinex_price,'
                                   'bitstamp_price, gdax_price, kraken_price',

                       'etheriumbtc': 'gemini_price, binance_price, bitfinex_price,'
                                       'bitstamp_price, gdax_price, kraken_price',

                       'litecoin': 'coinbase_price, binance_price, bitfinex_price,'
                                      'bitstamp_price, gdax_price, kraken_price',

                       'litecoinbtc': 'binance_price, bitfinex_price, bitstamp_price, gdax_price, kraken_price',

                       'ripplebtc': 'kraken_price, binance_price, bitfinex_price, bitstamp_price',

                       'monerobtc': 'kraken_price, binance_price, bitfinex_price',

                       'bitcashbtc': 'kraken_price, binance_price, bitfinex_price, bitstamp_price'

                       }

        search = ('SELECT id, ptime, {} FROM crypto_{} order by id desc limit {}'
                  .format(cprice_dict.get(self.table), self.table, tf))

        return self.db_search(search)

    def data_sources(self, tf):
        data, mdata = self.get_data(tf)

        gem_source = dict(time=[], y=[], ex=[])
        cb_source = dict(time=[], y=[], ex=[])
        kr_source = dict(time=[], y=[], ex=[])
        bi_source = dict(time=[], y=[], ex=[])
        bf_source = dict(time=[], y=[], ex=[])
        gd_source = dict(time=[], y=[], ex=[])
        bs_source = dict(time=[], y=[], ex=[])
        p_source = dict(time=[], profit=[], dir=[], color=[])

        gem_p, cb_p, kr_p, bi_p, bs_p, gd_p, bf_p = 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000

        exchanges = {'gemini_price': [gem_source, 'Gemini', 'gem', gem_p, 0.0025, 'blue'],
                     'coinbase_price': [cb_source, 'Coinbase', 'cb', cb_p, 0.0149, 'red'],
                     'kraken_price': [kr_source, 'Kraken', 'kr', kr_p, 0.0026, 'orange'],
                     'binance_price': [bi_source, 'Binance', 'bi', bi_p, 0.001, 'black'],
                     'bitfinex_price': [bf_source, 'Bitfinex', 'bf', bf_p, 0.002, 'green'],
                     'gdax_price': [gd_source, 'GDAX', 'gd', gd_p, 0.0025, 'yellow'],
                     'bitstamp_price': [bs_source, 'Bitstamp', 'bs', bs_p, 0.0025, 'purple']}

        data.sort(key=lambda x: x[0])

        for d in data:
            time = datetime.strptime(d[1], "%Y-%m-%d %H:%M:%S.%f")
            for x in range(2, len(d)):
                try:
                    exd = exchanges[mdata[x]]
                    p = float(d[x])

                    if p == 0.0:
                        price = 'nan'

                    else:
                        price = p

                    exd[3] = price
                    exd[0].get('y').append(price)
                    exd[0].get('ex').append(exd[1])
                    exd[0].get('time').append(time)

                except KeyError:
                    pass

            pdata = namedtuple('pdata', 'ex, p, f')
            prices = [pdata(*exchanges.get(z)[2:5]) for z in exchanges]
            profit, dir = CalcClass().get_profit(prices)
            p_source['profit'].append(profit)
            p_source['dir'].append(dir)
            p_source['time'].append(time)

            if profit > 0:
                color = "green"

            else:
                color = "red"

            p_source['color'].append(color)

        return exchanges, p_source

    def graph_data(self, tf=10):

        exchanges, p_source = self.data_sources(tf)

        if self.table in ('litecoinbtc', 'etheriumbtc', 'bitcashbtc', 'monerobtc', 'ripplebtc'):
            yf = '{0.0000000} BTC'

        else:
            yf = '{$0,0.00. USD}'

        hover = HoverTool(
            tooltips=[("price", '$y{}'.format(yf)),
                      ("Exchange", "@ex"),
                      ("Time", "@time{%m/%d %H:%M}")],

            formatters={"y": 'printf',
                        "time": 'datetime'}
        )

        hover_p = HoverTool(tooltips=[("profit", "@profit{}".format(yf)),
                                      ("Direction", "@dir"),
                                      ("Time", "@time{%m/%d %H:%M}")],

                            formatters= {"time": "datetime"},

                            mode="vline"
                            )

        p = figure(plot_width=1300, plot_height=500, x_axis_type="datetime", title="Price by Exchange")

        for exchange in exchanges:

            if exchanges[exchange][0].get('y'):
                source = exchanges[exchange][0]
                ex = exchanges[exchange][1]
                color = exchanges[exchange][5]

                p.line('time', 'y', source=source, legend=ex, line_width= 2, color=color)

            else:
                pass

        p.legend.click_policy = "hide"
        p.legend.location = "bottom_left"
        p.add_tools(hover)

        pd = figure(plot_width=1300, plot_height=300, x_axis_type="datetime", title="Arbitrage Profit or Loss")
        pd.line(x='time', y='profit', source=p_source, line_width=2, line_dash='dashed', line_color="black")
        pd.triangle(x='time', y='profit', source=p_source, size=10, fill_color='color')
        pd.add_tools(hover_p)
        script, div = components(column(pd, p))

        return script, div

if __name__ == "__main__":
    pass
    # a = GraphClass('etheriumbtc')
    # print(a.data_sources(10))
