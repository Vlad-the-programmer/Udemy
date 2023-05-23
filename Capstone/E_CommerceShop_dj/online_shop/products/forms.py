from django.forms import ModelForm
from .models import Product
from django import forms


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price']
        
        

