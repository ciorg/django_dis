import sqlite3
from datetime import datetime

from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import row, column
from bokeh.models import HoverTool
from bokeh.embed import components


class Bitcoin(object):

    def __init__(self):
        self.db = "../db.sqlite3"
        self.table = "crypto_bitcoin"

    def db_search(self, search):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        q = c.execute(search)
        data = [x for x in q]
        conn.close()
        return data

    def get_data(self):
        search = "SELECT * FROM {} WHERE id>20".format(self.table)
        return self.db_search(search)

    def graph_data(self):
        btc = self.get_data()
        gem_source = dict(x=[], y=[], ex=[], diff=[])
        cb_source = dict(x=[], y=[], ex=[], diff=[])
        p_source = dict(x=[], y=[], dir=[])

        for p in btc:
            t = datetime.strptime(p[1], "%Y-%m-%d %H:%M:%S.%f")
            gem_p = p[2]
            cb_p = p[3]
            gem_source['x'].append(t)
            gem_source['y'].append(gem_p)
            gem_source['ex'].append("Gemini")
            gem_source['diff'].append((gem_p - cb_p))

            cb_source['x'].append(t)
            cb_source['y'].append(cb_p)
            cb_source['ex'].append("Conbase")
            cb_source['diff'].append((cb_p - gem_p))

            fees = (gem_p * 0.0025) + (cb_p * .0149)
            net = abs(gem_p - cb_p)
            profit = net - fees

            if (gem_p * 0.0025) > (cb_p * 0.0149):
                dir = "CB->GEM"
            else:
                dir = "GEM->CB"

            p_source['x'].append(t)
            p_source['y'].append(profit)
            p_source['dir'].append(dir)

        output_file("test.html")

        hover = HoverTool(
            tooltips=[("price", "$y{$0,0.00}"),
                      ("Exchange", "@ex"),
                      ("Price Diff", "@diff{$0,0.00}")],
            formatters={"y": 'printf'}
        )

        hover_p = HoverTool(tooltips=[("profit", "$y{$0,0.00}"),
                                      ("Direction", "@dir")],
                            formatters={"y": 'printf'},
                            mode="vline")

        p = figure(plot_width=1000, plot_height=500, x_axis_type="datetime", x_axis_label="Time")
        p.line('x', 'y', source=gem_source, line_width=2, legend="Gemini", color="blue")
        p.line('x', 'y', source=cb_source, line_width=2, legend="Coinbase", color="orange")
        p.legend.click_policy = "hide"
        p.tools = [hover]

        pd = figure(plot_width=1000, plot_height=500, x_axis_type="datetime", x_axis_label="Time")
        pd.vbar(x='x', bottom=0, top='y', source=p_source, width=0.5, color="red", legend="Profit or Loss")
        pd.tools = [hover_p]

        script, div = components(column(p, pd))
        return script, div


if __name__ == "__main__":
    pass
