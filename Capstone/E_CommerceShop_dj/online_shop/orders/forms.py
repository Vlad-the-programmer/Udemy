from django import forms
from django.forms import ModelForm
from django.core.validators import MaxLengthValidator
from django.db import models

from .models import Order

class OrderCreateForm(ModelForm):
    phone = forms.CharField(max_length=15, 
                            validators=[
                                            MaxLengthValidator(limit_value=15)
                            ])
    
    class Meta:
        model = Order
        fields = ['quantity', 'address']
    
            
    def save(self, commit=True):
        order = super(OrderCreateForm, self).save(commit=False)
        
        order.check_quantity()
        
        products_prices = [product.price for product in order.products.all()]
        print(products_prices)
        total_order_cost = Order.objects.aggregate(total_cost=models.Sum("products__price"))['total_cost']
        print(total_order_cost)
        order.price = total_order_cost
        
        # customer_phone = order.customer.phone
        # if not order.phone:
        #     if customer_phone:
        #         order.phone = customer_phone
        #     else:
        #         raise ValueError("Your profile does not have a phone number, so you should provide one in this form, please!")
            
        customer_order_address = order.address
        if not customer_order_address:
            raise ValueError("You should provide us with your primary shipping address, please!")
        else:
            customer_order_splitted_address = customer_order_address.split()
            if len(customer_order_splitted_address) < 4:
                raise ValueError("Please check whether your shipping address contains a full name of your street as well as a number(with a big identification letter or without it) of your building and your apartment(or without if it is not a flat)!")
        if commit:
            # if not order.exists():
                super(OrderCreateForm, self).save()
                
        return order
        
class OrderUpdateForm(ModelForm):
        phone = forms.CharField(max_length=15, 
                                validators=[
                                                MaxLengthValidator(limit_value=15)
                                ])
        
        class Meta:
            model = Order
            fields = ['quantity', 'address']
            
        def save(self, commit=True):
            order = super().save(commit=False)
            order.check_quantity()
            
            if order.phone:
                order.customer.phone = self.phone
            # order.save(commit)
            return super(OrderCreateForm, self).save(commit)
