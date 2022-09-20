from django import forms
from django.forms import ModelForm

from .models import Order

class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'address', 'phone']
        
    def save(self, commit=True):
        order = super().save(commit=False)
        if order.quantity < 1:
            order.quantity = 0
        order.save()
        return order
        
        