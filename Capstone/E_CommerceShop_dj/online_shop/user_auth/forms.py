
from django.forms import ModelForm, TextInput
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Sign Up Form
class SignUpForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + ('phone', 'username', 'first_name', 'last_name', 'email')
        
        # def __init__(self, *args, **kwargs):
        #     super(SignUpForm, self).__init__(*args, **kwargs)
            # for name, field in self.fields.items():
            #     field.widget.attrs.update({'class': 'input'})


# Login Up Form
class LoginForm(ModelForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address', widget=TextInput)
    password = forms.CharField(max_length=100, widget=TextInput)
    class Meta:
        model = Customer
        fields = [
            'email',
            'password',
            ]
