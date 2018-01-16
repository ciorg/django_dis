from time import sleep
import argparse
from add_price_data import AddPriceDataClass


def activate(coin):
    while True:
        apd = AddPriceDataClass(coin)
        apd.threaded_call()
        print(apd.prices_dict)
        apd.add_to_db()
        # apd.db_check()
        sleep(5)

parser = argparse.ArgumentParser(description='Runs the add data script')
parser.add_argument("-go", help="Adds price data to the db, pick a coin to add", nargs=1,
                    choices=['btc', 'eth', 'ethbtc', 'ltc', 'ltcb', 'bchb', 'xmrb', 'xrpb'])

args = parser.parse_args()
coin = args.go[0]

activate(coin)
