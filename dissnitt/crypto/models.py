from django.db import models


class Bitcoin(models.Model):
    ptime = models.DateTimeField()
    gemini_price = models.DecimalField(max_digits=20, decimal_places=4)
    coinbase_price = models.DecimalField(max_digits=20, decimal_places=4)
