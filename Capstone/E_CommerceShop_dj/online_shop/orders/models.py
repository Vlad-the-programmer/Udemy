from django.db import models
import datetime
import uuid  

from django.core import validators
from user_auth.models import Customer
from products.models import Product

class Order(models.Model):
    # order_id = models.UUIDField("An Order id", primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, related_name='customer',
                                on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=4, decimal_places=2,
                                null=False, 
                                blank=False)
    address = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=12, default='', blank=True)
    date_created = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


