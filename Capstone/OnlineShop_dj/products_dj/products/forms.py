from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Enter a first name')
    last_name = forms.CharField(max_length=30, required=False, help_text='Enter a last name')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            ]

class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['status']


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerCreateForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
