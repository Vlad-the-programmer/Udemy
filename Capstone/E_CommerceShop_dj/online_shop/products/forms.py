from email import message
from django.forms import ModelForm, TextInput, Textarea
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core import validators


# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                help_text='Enter a first name', 
                                widget=TextInput)
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Enter a last name',
                                 widget=TextInput)
    username = forms.CharField(max_length=50, required=True, 
                                help_text='Enter an username ',
                                 widget=TextInput)
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address', 
                                            validators=[validators.EmailValidator],
                                             required=True, widget=TextInput)
    password = forms.CharField(max_length=100, help_text='Enter a password', required=True,
                                                                         widget=TextInput)
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            
            ]


# Login Up Form
class LoginForm(ModelForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address', widget=TextInput)
    password = forms.CharField(max_length=100, widget=TextInput)
    class Meta:
        model = User
        fields = [
            'email',
            'password',
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
