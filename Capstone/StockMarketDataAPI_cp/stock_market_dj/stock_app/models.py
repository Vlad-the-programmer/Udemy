from django.db import models


class CurrencyExchange(models.Model):
    id = models.BigAutoField(primary_key=True)
    base_currency = models.CharField(max_length=3, null=True, default=0, unique=True)
    change_for_currency = models.CharField(max_length=3, null=True, default=0, unique=True)
    amount = models.FloatField('The amount to exchange', null=True, default=0)
    exchanged_amount = models.FloatField('The amount after the exchange', default=0, null=True)

    def get_absolute_url(self):
        return ''

    def __repr__(self):
        return f'{self.id} {self.base_currency} {self.change_for_currency} {self.amount} {self.exchanged_amount}'

