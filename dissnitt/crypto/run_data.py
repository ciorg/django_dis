from time import sleep
import argparse
from add_price_data import AddPriceDataClass


def activate(coin, exchanges='all'):
    # while True:
    apd = AddPriceDataClass(coin, exchanges)
    #apd.threaded_call()
    #apd.add_to_db()
    apd.db_check()
    #sleep(5)

parser = argparse.ArgumentParser(description='Runs the add data script')
parser.add_argument("-go", help="Adds price data to the db, pick a coin to add", nargs=1,
                    choices=['btc', 'eth', 'ethbtc'])

args = parser.parse_args()

if args.go[0] == 'eth':
    activate('eth')

elif args.go[0] == 'btc':
    activate('btc')

elif args.go[0] == 'ethbtc':
    activate('ethb', 'ethb')

else:
    print("nothing to do here")


