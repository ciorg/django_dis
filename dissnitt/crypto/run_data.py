from time import sleep
import argparse
from add_price_data import AddPriceDataClass


def activate(coin):
    while True:
        apd = AddPriceDataClass(coin)
        apd.threaded_call()
        apd.add_to_db()
        sleep(5)

parser = argparse.ArgumentParser(description='Runs the add data script')
parser.add_argument("-go", help="Adds price data to the db, pick a coin to add", nargs=1,
                    choices=['btc', 'eth'])

args = parser.parse_args()

if args.go[0] == 'eth':
    activate('eth')

elif args.go[0] == 'btc':
    activate('btc')

else:
    print("nothing to do here")


