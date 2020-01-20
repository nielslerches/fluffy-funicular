from django.db import models

from shared.models import TimestampedModel


class Customer(TimestampedModel, models.Model):
    pass


class CartItem(TimestampedModel, models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sales_channel = models.ForeignKey('catalog.SalesChannel', on_delete=models.CASCADE)
    article = models.ForeignKey('catalog.Article', on_delete=models.CASCADE)
    quantity = models.IntegerField()
