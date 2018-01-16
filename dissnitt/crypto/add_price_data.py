import threading, logging
import sqlite3
from datetime import datetime
from exchanges import Exchanges


class AddPriceDataClass(object):

    def __init__(self, coin):

        cd_dict = {'btc': ('crypto_bitcoin',('cb', 'gem', 'kr', 'bi', 'bf', 'bs', 'gd')),
                      'eth': ('crypto_etherium', ('cb', 'gem', 'kr', 'bi', 'bf', 'bs', 'gd')),
                      'ethb': ('crypto_etheriumbtc', ('gem', 'kr', 'bi', 'bf', 'bs', 'gd')),
                      'ltc': ('crypto_litecoin', ('cb', 'kr', 'bi', 'bf', 'bs', 'gd')),
                      'ltcb': ('crypto_litecoinbtc', ('kr', 'bi', 'bf', 'bs', 'gd')),
                      'xrpb': ('crypto_ripplebtc', ('kr', 'bi', 'bf', 'bs')),
                      'xmrb': ('crypto_monerobtc', ('kr', 'bi', 'bf')),
                      'bchb': ('crypto_bitcashbtc', ('kr', 'bi', 'bf', 'bs'))
                      }

        logging.basicConfig(filename='logs/data.log', level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

        self.coin = coin
        self.exchanges = cd_dict.get(coin)[1]
        self.table = cd_dict.get(coin)[0]
        self.prices_dict = {}

    def get_price(self, exchange):
        p_dict = {'bi': 'Exchanges("{}").binance()',
                  'bf': 'Exchanges("{}").bitfinex()',
                  'bs': 'Exchanges("{}").bitstamp()',
                  'cb': 'Exchanges("{}").coinbase()',
                  'gd': 'Exchanges("{}").gdax()',
                  'gem': 'Exchanges("{}").gemini()',
                  'kr': 'Exchanges("{}").kraken()',
                  }

        call = eval(p_dict.get(exchange).format(self.coin))
        self.prices_dict[exchange] = call

    def threaded_call(self):
        threads = []
        for e in self.exchanges:
            t = threading.Thread(target=self.get_price, args=(e,))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def run(self):
        self.threaded_call()

    def db_search(self, search):
        conn = sqlite3.connect("../db.sqlite3")
        c = conn.cursor()
        c.execute(search)
        data = c.fetchall()
        mdata = [x[0] for x in c.description]
        conn.close()
        return data, mdata

    def last_id(self):
        id_search = 'SELECT id FROM {} order by id desc limit 1;'.format(self.table)
        last, desc = self.db_search(id_search)

        try:
            lid = last[0][0]

        except IndexError:
            lid = 0

        return lid

    def add_to_db(self):

        lid = self.last_id()

        data = [lid+1, datetime.now()] + [self.prices_dict.get(ex) for ex in self.exchanges]

        conn = sqlite3.connect("../db.sqlite3")
        c = conn.cursor()

        model_col_dict = {'gem': 'gemini_price',
                          'cb': 'coinbase_price',
                          'bi': 'binance_price',
                          'bf': 'bitfinex_price',
                          'bs': 'bitstamp_price',
                          'gd': 'gdax_price',
                          'kr': 'kraken_price'}

        col_fields = ",".join([model_col_dict.get(ex) for ex in self.exchanges])
        col_fields = "id, ptime, " + col_fields.strip(",")

        q_values = "?,"*(len(self.exchanges)+2)
        q_values = q_values.strip(",")

        search = 'INSERT INTO {} ({}) VALUES({})'.format(self.table, col_fields, q_values)

        try:
            c.execute(search, data)
            conn.commit()
            conn.close()
            logging.info("added data: {}".format(",".join([str(x) for x in data])))

        except Exception as e:
            logging.exception("{}".format(e))

    def db_check(self):
        search = 'SELECT * FROM {}'.format(self.table)
        data, mdata = self.db_search(search)
        print(data, mdata)


if __name__ == "__main__":
    pass