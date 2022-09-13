from django.db import models
from django.core import validators
from django.contrib.auth.validators import UnicodeUsernameValidator
from .managers import UserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Gender(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")
    OTHER = "other", _("Other")

    
class Customer(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    # id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=10, default='', null=True,  blank=True)
    email = models.EmailField(validators=[validators.EmailValidator()], unique=True)
    description  = models.TextField(max_length=1000,blank=True, null=True)
    gender = models.CharField('Gender', max_length=10, choices=Gender.choices,
                                default='Male', null=True)
    
    featured_img = models.ImageField(verbose_name='A profile image',
                                     upload_to='profiles', 
                                     default='products/profile_default.jpg')
    
    password = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.email} {self.username} {self.customer_id}'
    
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
        # unique_together = ['email']


class Profile(models.Model):
    # USERNAME_FIELD = 'email'
    
    profile_id = models.AutoField(primary_key=True)
    # username = models.CharField(max_length=50,blank=True, null=True)
    # first_name = models.CharField(max_length=50, null=True, blank=True)
    # last_name = models.CharField(max_length=50, null=True, blank=True)
    # phone = models.CharField(max_length=10, default='', null=True,  blank=True)
    # email = models.EmailField(validators=[validators.EmailValidator()])
    # password = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                    related_name="customer", null=True)
    # gender = models.CharField('Gender', max_length=10, choices=Gender.choices,
    #                             default='Male')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        # unique_together = ['email']

    def __str__(self):
        return f' {self.profile_id}'
    
    def profile_exists(self, email):
        profile = Profile.objects.filter(email=email)
        if profile.exists():
            return True
        return False
        