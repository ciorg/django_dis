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
        q = c.execute(search)
        data = [x for x in q]
        conn.close()
        return data

    def get_data(self, tf):
        # search = "SELECT * FROM {} where ptime > datetime('now', '-31 hours', '-5 minutes')".format(self.table)
        search = ('SELECT id, ptime, gemini_price, coinbase_price, binance_price, bitfinex_price, bitstamp_price, gdax_price,'
                  'kraken_price FROM crypto_{} order by id desc limit {}'.format(self.table, tf))

        return self.db_search(search)


    def graph_data(self, tf=60):
        price_data = self.get_data(tf)
        gem_source, cb_source, kr_source = dict(y=[], ex=[]),  dict(y=[], ex=[]), dict(y=[], ex=[])
        bi_source, bf_source = dict(y=[], ex=[]), dict(y=[], ex=[])
        gd_source, bs_source = dict(y=[], ex=[]), dict(y=[], ex=[])
        p_source = dict(profit=[], dir=[], color=[])
        time = []

        price_data.sort(key=lambda x: x[0])

        for p in price_data:
            t = datetime.strptime(p[1], "%Y-%m-%d %H:%M:%S.%f")
            time.append(t)

            checked_v = [v if float(v) != 1.001 else 'nan' for v in p[2:9]]

            gem_p, cb_p, bi_p, bf_p, bs_p, gd_p, kr_p = checked_v

            gem_source['y'].append(gem_p)
            gem_source['ex'].append("Gemini")

            cb_source['y'].append(cb_p)
            cb_source['ex'].append("Coinbase")

            kr_source['y'].append(kr_p)
            kr_source['ex'].append("Kraken")

            bi_source['y'].append(bi_p)
            bi_source['ex'].append("Binance")

            bf_source['y'].append(bf_p)
            bf_source['ex'].append("Bitfinex")

            bs_source['y'].append(bs_p)
            bs_source['ex'].append("Bitstamp")

            gd_source['y'].append(gd_p)
            gd_source['ex'].append("GDAX")

            pdata = namedtuple('pdata', 'ex, p, f')

            prices = (pdata("cb", cb_p, 0.0149),
                      pdata("gem", gem_p, 0.0025),
                      pdata("kr", kr_p, 0.0026),
                      pdata('bi', bi_p, 0.001),
                      pdata('bf', bf_p, 0.002),
                      pdata('bs', bs_p, 0.0025),
                      pdata('gd', gd_p, 0.0025))

            profit, dir = CalcClass().get_profit(prices)

            p_source['profit'].append(profit)
            p_source['dir'].append(dir)

            if profit > 0:
                color = "green"

            else:
                color = "red"

            p_source['color'].append(color)

        # output_file("test.html")

        hover = HoverTool(
            tooltips=[("price", "$y{$0,0.00}"),
                      ("Exchange", "@ex"),
                      ("Time", "@time{%m/%d %H:%M}")],

            formatters={"y": 'printf',
                        "time": 'datetime'}
        )

        hover_p = HoverTool(tooltips=[("profit", "@profit{$0,0.00}"),
                                      ("Direction", "@dir"),
                                      ("Time", "@time{%m/%d %H:%M}")],

                            formatters= {"time": "datetime"},

                            mode="vline"
                            )

        gem_source['time'] = cb_source['time'] = kr_source['time'] = p_source['time'] = bi_source['time'] = time
        bf_source['time'] = bs_source['time'] = gd_source['time'] = time

        p = figure(plot_width=1300, plot_height=500, x_axis_type="datetime", title="Bitcoin Price by Exchange")
        p.line('time', 'y', source=gem_source, line_width=2, legend="Gemini", color="blue")
        p.line('time', 'y', source=cb_source, line_width=2, legend="Coinbase", color="orange")
        p.line('time', 'y', source=kr_source, line_width=2, legend="Kraken", color="green")
        p.line('time', 'y', source=bi_source, line_width=2, legend="Binance", color="black")
        p.line('time', 'y', source=bf_source, line_width=2, legend="Bitfinex", color="yellow")
        p.line('time', 'y', source=bs_source, line_width=2, legend="Bitstamp", color="purple")
        p.line('time', 'y', source=gd_source, line_width=2, legend="GDAX", color="red")

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
