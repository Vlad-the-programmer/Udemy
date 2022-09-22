from django.db import models
import datetime
import uuid  

from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core import validators
from user_auth.models import Customer
from products.models import Product

class Order(models.Model):
    order_id = models.UUIDField(_("An Order id"),
                                primary_key=True,
                                default=uuid.uuid4,
                                editable=False)
    # order_id = models.AutoField(primary_key=True)
    slug = models.SlugField(null=True, blank=True)
    customer =  models.ForeignKey(Customer, 
                                on_delete=models.CASCADE,
                                related_name="orderer",
                                null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=4,
                                decimal_places=2,
                                null=True, 
                                blank=True)
    address = models.CharField(max_length=50, null=False, blank=False)
    # phone = models.CharField(max_length=12, default='', blank=True)
    date_created = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    products = models.ManyToManyField("products.Product",
                                      verbose_name=_("Ordered products"),
                                      related_name='products')

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def check_quantity(self):
        if self.quantity < 1:
            self.quantity = 0

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer__customer_id=customer_id).order_by('-date')

    @property
    def set_default_slug(self):
        return slugify(f'{self.customer.first_name} - {self.date_created} - {self.order_id}')
    
    # def exists(self):
    #     order = Order.objects.filter()