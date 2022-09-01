from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.contrib.auth.validators import UnicodeUsernameValidator
from .managers import UserManager


class Customer(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    # id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    cutomer_id = models.AutoField(primary_key=True)
    # profile = models.OneToOneField("Profile", related_name="profile",
    #                                on_delete=models.CASCADE, null=True)
    
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=10, default='', null=True,  blank=True)
    email = models.EmailField(validators=[validators.EmailValidator()],
                              unique=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.email} {self.username}'
    
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def exists(self):
        if Customer.objects.filter(email=self.email):
            return True

        return False

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=10, default='', null=True, blank=True)
    description  = models.TextField(max_length=1000,blank=True, null=True)
    email = models.EmailField(validators=[validators.EmailValidator()])
    password = models.CharField(max_length=100, null=True, blank=True)
    featured_img = models.ImageField(verbose_name='A profile image',
                                     upload_to='profiles', 
                                     default='products/profile_default.jpg')
    
    owner = models.OneToOneField(Customer, related_name='owner',
                                 on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=30, null=True, blank=True,
                                validators=[UnicodeUsernameValidator()])
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
