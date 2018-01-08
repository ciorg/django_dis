from django.db import models


class Bitcoin(models.Model):
    ptime = models.DateTimeField()
    gemini_price = models.DecimalField(max_digits=20, decimal_places=4)
    coinbase_price = models.DecimalField(max_digits=20, decimal_places=4)
    kraken_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.0000)
    binance_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.0000)
    bitfinex_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.0000)
    bitstamp_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.0000)
    gdax_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.0000)
