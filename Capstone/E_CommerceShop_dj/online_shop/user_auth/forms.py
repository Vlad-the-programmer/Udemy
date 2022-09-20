
from django.forms import ModelForm, TextInput
from .models import Customer, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import password_validation

# Sign Up Form
class SignUpForm(UserCreationForm):
    
    class Meta(UserCreationForm):
        model = Customer
        fields = ('username', 'phone', 'first_name', 'last_name', 'email', 'featured_img') 
        error_class = 'error'
        
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


class ProfileUpdateForm(UserChangeForm):
   
    class Meta:
        model = Customer
        fields = ('username', 'phone', 'first_name', 'last_name', 'email', 'featured_img', 'description', 'gender')
        error_class = 'error'
        
    def save(self, commit=True):
        customer = super().save(commit=False)
        
        email = self.cleaned_data.get('email')
        customer.email = email.lower()
        # customer.password = customer.set_password(self.cleaned_data['password1'])
        
        if commit:
            if customer.exists():
                super(ProfileUpdateForm, self).save()
                return customer
            
            