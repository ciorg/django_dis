import threading
import sqlite3
from datetime import datetime
from time import sleep
from exchanges import Exchanges


class BitCoinPrice(object):
    def __init__(self):
        self.exchanges = ('cb', 'gem', 'kr', 'bi')
        self.prices_dict = {}

    def get_price(self, exchange, coin):
        p_dict = {'bi': 'Exchanges("{}").binance()',
                  'cb': 'Exchanges("{}").coinbase()',
                  'gem': 'Exchanges("{}").gemini()',
                  'kr': 'Exchanges("{}").kraken()'
                  }

        line = p_dict.get(exchange).format(coin)
        print(line)
        call = eval(p_dict.get(exchange).format(coin))
        self.prices_dict[exchange] = call

    def threaded_call(self):
        threads = []
        for e in self.exchanges:
            t = threading.Thread(target=self.get_price, args=(e, "btc"))
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
        id_search = '''SELECT id FROM crypto_bitcoin order by id desc limit 1;'''
        last = self.db_search(id_search)

        try:
            lid = last[0][0]

        except IndexError:
            lid = 0

        data = [lid+1, datetime.now(), self.prices[0], self.prices[1], self.prices[2]]
        conn = sqlite3.connect("../db.sqlite3")
        c = conn.cursor()
        c.execute('INSERT INTO crypto_bitcoin VALUES(?, ?, ?, ?, ?)', data)
        conn.commit()
        conn.close()
        print("added more data: {}, {}, {}, {}, {}".format(*data))

    def db_check(self):
        search = '''SELECT * FROM crypto_bitcoin'''
        sdata = self.db_search(search)
        for x in sdata:
            print(x)


if __name__ == "__main__":
    # while True:
    p = BitCoinPrice()
    p.threaded_call()
    # p.get_price('bi', 'btc')
    print(p.prices_dict)
        # p.add_to_db()
        # sleep(60)
