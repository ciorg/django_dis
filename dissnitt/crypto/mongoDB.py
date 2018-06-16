from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.cryptoData

prices = db.prices
# one = prices.find_one()
count = prices.count()
print(count)
# filter by coin, denomination, exchange, timestamp
# inBTC = prices.find({ 'denomination': 'USD  ' })
inUSD = prices.find({ 'denomination': 'USD'})

for doc in inUSD:
    print(doc)
