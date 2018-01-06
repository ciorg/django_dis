import sqlite3
from datetime import datetime
from collections import namedtuple

from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import row, column
from bokeh.models import HoverTool
from bokeh.embed import components


class Bitcoin(object):

    def __init__(self):
        self.db = "db.sqlite3"
        self.table = "crypto_bitcoin"

    def db_search(self, search):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        q = c.execute(search)
        data = [x for x in q]
        conn.close()
        return data

    def get_data(self):
        # search = "SELECT * FROM {} where ptime > datetime('now', '-31 hours', '-5 minutes')".format(self.table)
        search = "SELECT * FROM {} order by id desc limit 60".format(self.table)
        return self.db_search(search)

    def safety_check(self, mode, p):
        if  p < mode*0.5:
            return mode
        else:
            return p

    def get_profit(self, prices):

        high = -10000
        hp_data = tuple()
        for x in range(len(prices), 0, -1):
            if x >= 2:
                p1, f1 = prices[x - 1].p, prices[x - 1].f

                for y in range(x - 1, 0, -1):
                    p2, f2 = prices[y - 1].p, prices[y - 1].f

                    profit = abs(p1 - p2) - ((p1 * f1) + (p2 * f2))

                    if profit > high:
                        high = profit
                        dir = [prices[x - 1], prices[y - 1]]
                        dir.sort(reverse=True, key=lambda x: x.p)
                        hp_data = (profit, "{}->{}".format(dir[0].ex, dir[1].ex))

            else:
                pass

        return hp_data

    def graph_data(self):
        btc = self.get_data()
        gem_source = dict(y=[], ex=[])
        cb_source = dict(y=[], ex=[])
        kr_source = dict(y=[], ex=[])
        p_source = dict(profit=[], dir=[], color=[])
        time = []

        for p in btc:
            t = datetime.strptime(p[1], "%Y-%m-%d %H:%M:%S.%f")
            time.append(t)

            gem_p, cb_p, kr_p = p[2], p[3], p[4]

            med_v = [gem_p, cb_p, kr_p]
            med_v.sort()
            mode = med_v[1]

            gem_p = self.safety_check(mode, gem_p)
            cb_p = self.safety_check(mode, cb_p)
            kr_p = self.safety_check(mode, kr_p)

            gem_source['y'].append(gem_p)
            gem_source['ex'].append("Gemini")

            cb_source['y'].append(cb_p)
            cb_source['ex'].append("Coinbase")

            kr_source['y'].append(kr_p)
            kr_source['ex'].append("Kraken")

            pdata = namedtuple('pdata', 'ex, p, f')

            prices = (pdata("cb", cb_p, 0.0149),
                      pdata("gem", gem_p, 0.0025),
                      pdata("kr", kr_p, 0.0026))

            profit, dir = self.get_profit(prices)

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

        gem_source['time'] = cb_source['time'] = kr_source['time'] = p_source['time'] = time

        p = figure(plot_width=1300, plot_height=500, x_axis_type="datetime", title="Bitcoin Price by Exchange")
        p.line('time', 'y', source=gem_source, line_width=2, legend="Gemini", color="blue")
        p.line('time', 'y', source=cb_source, line_width=2, legend="Coinbase", color="orange")
        p.line('time', 'y', source=kr_source, line_width=2, legend="Kraken", color="green")
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
