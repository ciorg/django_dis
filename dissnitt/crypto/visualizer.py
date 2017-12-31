import sqlite3
from datetime import datetime

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
        search = "SELECT * FROM {} where ptime > datetime('now', '-31 hours', '-5 minutes')".format(self.table)
        return self.db_search(search)

    def graph_data(self):
        btc = self.get_data()
        gem_source = dict(x=[], y=[], ex=[])
        cb_source = dict(x=[], y=[], ex=[])
        kr_source = dict(x=[], y=[], ex=[])
        p_source = dict(time=[], profit=[], dir=[], color=[])

        for p in btc:
            t = datetime.strptime(p[1], "%Y-%m-%d %H:%M:%S.%f")
            gem_p = p[2]
            cb_p = p[3]
            kr_p = p[4]

            gem_source['x'].append(t)
            gem_source['y'].append(gem_p)
            gem_source['ex'].append("Gemini")

            cb_source['x'].append(t)
            cb_source['y'].append(cb_p)
            cb_source['ex'].append("Coinbase")

            kr_source['x'].append(t)
            kr_source['y'].append(kr_p)
            kr_source['ex'].append("Kraken")

            pdata = [(gem_p, 0.0025, "GEM"),
                     (cb_p, 0.0149, "CB"),
                     (kr_p, 0.0026, "KR")]

            pdata.sort(key=lambda x: x[0])

            profit = (pdata[-1][0] - pdata[0][0]) - ((pdata[-1][0] * pdata[-1][1]) + (pdata[0][0] * pdata[0][1]))
            if profit > 0:
                color = "green"

            else:
                color = "red"

            dir = "{}->{}".format(pdata[0][2], pdata[-1][2])

            p_source['time'].append(t)
            p_source['profit'].append(profit)
            p_source['dir'].append(dir)
            p_source['color'].append(color)

        # output_file("test.html")

        hover = HoverTool(
            tooltips=[("price", "$y{$0,0.00}"),
                      ("Exchange", "@ex")],
            formatters={"y": 'printf'}
        )

        hover_p = HoverTool(tooltips=[("profit", "@profit{$0,0.00}"),
                                      ("Direction", "@dir")],
                            mode="vline"
                            )

        p = figure(plot_width=1300, plot_height=500, x_axis_type="datetime", title="Bitcoin Price by Exchange")
        p.line('x', 'y', source=gem_source, line_width=2, legend="Gemini", color="blue")
        p.line('x', 'y', source=cb_source, line_width=2, legend="Coinbase", color="orange")
        p.line('x', 'y', source=kr_source, line_width=2, legend="Kraken", color="green")
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
