from django.db import models


class Bitcoin(models.Model):
    ptime = models.DateTimeField()
    gemini_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    coinbase_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    kraken_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    binance_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    bitfinex_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    bitstamp_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    gdax_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)


class Etherium(models.Model):
    ptime = models.DateTimeField()
    gemini_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    coinbase_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    kraken_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    binance_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    bitfinex_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    bitstamp_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    gdax_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)


class EtheriumBTC(models.Model):
    ptime = models.DateTimeField()
    gemini_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    kraken_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    binance_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    bitfinex_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    bitstamp_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    gdax_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)


class Litecoin(models.Model):
    ptime = models.DateTimeField()
    coinbase_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.000)
    kraken_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    binance_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    bitfinex_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    bitstamp_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    gdax_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)


class LitecoinBTC(models.Model):
    ptime = models.DateTimeField()
    kraken_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    binance_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    bitfinex_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    bitstamp_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    gdax_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)


class RippleBTC(models.Model):
    ptime = models.DateTimeField()
    kraken_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    binance_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    bitfinex_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    bitstamp_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)


class MoneroBTC(models.Model):
    ptime = models.DateTimeField()
    kraken_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    binance_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    bitfinex_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)


class BitcashBTC(models.Model):
    ptime = models.DateTimeField()
    kraken_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    binance_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    bitfinex_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
    bitstamp_price = models.DecimalField(max_digits=20, decimal_places=6, default=0.000)
