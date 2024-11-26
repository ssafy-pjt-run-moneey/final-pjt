from django.db import models

class ExchangeRate(models.Model):
    currency_code = models.CharField(max_length=10)
    currency_name = models.CharField(max_length=50)
    deal_base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    date_fetched = models.DateField(auto_now_add=True)