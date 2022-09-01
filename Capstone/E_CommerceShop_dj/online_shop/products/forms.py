from django.forms import ModelForm
from .models import Product
from django import forms


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

