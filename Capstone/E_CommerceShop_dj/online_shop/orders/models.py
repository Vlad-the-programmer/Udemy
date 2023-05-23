from django.db import models
import datetime
import uuid  

from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):
    order_id = models.UUIDField(_("An Order id"),
                                primary_key=True,
                                default=uuid.uuid4,
                                editable=False)
    slug = models.SlugField(null=True, blank=True, max_length=100)
    customer =  models.ForeignKey("user_auth.Customer", 
                                on_delete=models.CASCADE,
                                related_name="orderer",
                                null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.slug} {self.complete}'
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @staticmethod
    def get_orders_by_customer(customer_id, complete):
        return Order.objects.filter(customer__customer_id=customer_id, complete=complete).order_by('-date')

    @property
    def set_default_slug(self):
        return slugify(f'{self.date_ordered} - {self.order_id}')
    
    @property
    def get_cart_items(self):
        try:
            orderitems = self.orderitem_set.all().count()
        except:
            orderitems = 0  
        return orderitems

    @property
    def get_order_items(self):
        orderitems = self.orderitem_set.all()
        return orderitems

class OrderItem(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.SET_NULL,
                                                        null=True, blank=True)
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL,
                                                        null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('OrderItem')
        verbose_name_plural = _('OrderItems')
        unique_together = ["product"]
    
    def __str__(self):
        return self.product.name
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    @property
    def imageURL(self):
        try:
            url = self.product.image.url
        except:
            url = ''
        return url
        
class ShippingAddress(models.Model):
    customer = models.ForeignKey("user_auth.Customer", on_delete=models.SET_NULL,
                                                                    null=True)
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, 
                                                                    null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('ShippingAddress')
        verbose_name_plural = _('ShippingAddresses')
        
    def __str__(self):
        return self.address