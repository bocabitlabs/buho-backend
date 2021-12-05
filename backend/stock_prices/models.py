from enum import unique
from django.db import models
from djmoney.models.fields import MoneyField


class StockPrice(models.Model):
    company_name = models.CharField(max_length=200)
    price = MoneyField(max_digits=29, decimal_places=19, default_currency=None)
    transaction_date = models.DateField()
    ticker = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str___(self):
        return "{} - {} ({})".format(self.ticker, self.price, self.transaction_date)

    class Meta:
        unique_together = ("ticker", "transaction_date")