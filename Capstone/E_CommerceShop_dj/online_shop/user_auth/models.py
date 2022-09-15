from django.db import models
from django.core import validators
from django.contrib.auth.validators import UnicodeUsernameValidator
from .managers import UserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class Gender(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")
    OTHER = "other", _("Other")

    
class Customer(AbstractUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    # id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=10, default='', null=True,  blank=True)
    email = models.EmailField(validators=[validators.EmailValidator()],
                                                            unique=True)
    description  = models.TextField(max_length=1000,blank=True, null=True)
    gender = models.CharField(_('Gender'), max_length=10, choices=Gender.choices,
                                default=_('Male'), null=True)
    
    featured_img = models.ImageField(verbose_name=_('A profile image'),
                                     upload_to='profiles', 
                                     default='products/profile_default.jpg')
    
    password = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        # unique_together = ['email']

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
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.username

class Profile(models.Model):
    # USERNAME_FIELD = 'email'
    
    profile_id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                    related_name="customer", null=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f' {self.profile_id}'
    
    def profile_exists(self, email):
        profile = Profile.objects.filter(email=email)
        if profile.exists():
            return True
        return False
        