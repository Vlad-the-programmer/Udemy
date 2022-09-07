
from django.forms import ModelForm, TextInput
from .models import Customer, Profile
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import password_validation

# Sign Up Form
class SignUpForm(UserCreationForm):

    class Meta:
        model = Customer
        fields = ('username','phone', 'first_name', 'last_name', 'email', 'featured_img') 
        
        # def __init__(self, *args, **kwargs):
        #     super(SignUpForm, self).__init__(*args, **kwargs)
            # for name, field in self.fields.items():
            #     field.widget.attrs.update({'class': 'input'})

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # user.profile.description = self.cleaned_data['description']
        if commit:
            user.save()

        return user

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


class ProfileUpdateForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
        required=False
    )
    class Meta:
        model = Customer
        fields = ('username', 'phone', 'first_name', 'last_name', 'email', 'featured_img', 'description', 'gender')
        
    def save(self, commit=True, force_insert=False, force_update=True):
        customer = super().save(commit=False)
        
        email = self.cleaned_data.get('email')
        customer.email = email.lower()
        customer.password = customer.set_password(self.cleaned_data['password1'])
        if commit:
            # profile = Profile.objects.filter(email=profile.email)
            if not customer.exists():
                super(ProfileUpdateForm, self).save(force_insert, force_update)
            
        return customer