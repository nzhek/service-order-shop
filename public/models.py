from django.db import models
from django.utils import timezone


class Customer(models.Model):
    title = models.CharField(default='', max_length=255)

    def __str__(self):
        return "{}".format(self.title)


class Order(models.Model):
    customer = models.ForeignKey(Customer, blank=None, on_delete=models.CASCADE)
    amount_price = models.CharField(default='', max_length=255)
    created = models.DateTimeField(editable=False, default=timezone.now)

    def __str__(self):
        return "{}:{}".format(self.customer.title, self.amount_price)
