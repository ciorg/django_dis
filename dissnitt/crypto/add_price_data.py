import threading, logging
import sqlite3
from datetime import datetime
from time import sleep
from exchanges import Exchanges


class BitCoinPrice(object):

    def __init__(self, coin):
        self.exchanges = ('cb', 'gem', 'kr', 'bi', 'bf', 'bs', 'gd')
        self.prices_dict = {}
        logging.basicConfig(filename='logs/data.log', level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

        self.coin = coin
        table_dict = {'btc': 'crypto_bitcoin',
                      'eth': 'crypto_etherium'}

        self.table = table_dict.get(coin)

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
        q = c.execute(search)
        data = [x for x in q]
        conn.close()
        return data

    def add_to_db(self):
        id_search = 'SELECT id FROM {} order by id desc limit 1;'.format(self.table)
        last = self.db_search(id_search)

        try:
            lid = last[0][0]

        except IndexError:
            lid = 0

        data = [lid+1, datetime.now(), self.prices_dict.get('gem'), self.prices_dict.get('cb'),
                self.prices_dict.get('bi'), self.prices_dict.get('bf'), self.prices_dict.get('bs'),
                self.prices_dict.get('gd'), self.prices_dict.get('kr')]

        conn = sqlite3.connect("../db.sqlite3")
        c = conn.cursor()
        try:
            c.execute('INSERT INTO {} (id, ptime, gemini_price, coinbase_price, binance_price, bitfinex_price,'
                      'bitstamp_price, gdax_price, kraken_price) '
                      'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'.format(self.table), data)

            conn.commit()
            conn.close()
            logging.info("added data: {}, {}, {}, {}, {}, {}, {}, {}, {}".format(*data))

        except Exception as e:
            logging.exception("{}".format(e))

    def db_check(self):
        search = 'SELECT * FROM {}'.format(self.table)
        sdata = self.db_search(search)
        for x in sdata:
            print(x)


if __name__ == "__main__":
    pass