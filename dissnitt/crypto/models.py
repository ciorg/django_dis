from django.db import models


class Bitcoin(models.Model):
    ptime = models.DateTimeField()
    gemini_price = models.DecimalField(max_digits=20, decimal_places=4, default=1.001)
    coinbase_price = models.DecimalField(max_digits=20, decimal_places=4, default=1.001)
    kraken_price = models.DecimalField(max_digits=20, decimal_places=4, default=1.001)
    binance_price = models.DecimalField(max_digits=20, decimal_places=4, default=1.001)
    bitfinex_price = models.DecimalField(max_digits=20, decimal_places=4, default=1.001)
    bitstamp_price = models.DecimalField(max_digits=20, decimal_places=4, default=1.001)
    gdax_price = models.DecimalField(max_digits=20, decimal_places=4, default=1.001)
