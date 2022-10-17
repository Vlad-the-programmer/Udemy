from django.db import models

import uuid  

from django.core import validators
from user_auth.models import Customer
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Product(models.Model):
    
    product_id = models.UUIDField(_("A Product id"), primary_key=True, default=uuid.uuid4,
                                  editable=False)
    
    name = models.CharField(max_length=30, null=False, blank=False)
    slug = models.SlugField(null=True, blank=True, max_length=100)
    description  = models.TextField(max_length=1000,blank=True, null=True)
    customer =  models.ForeignKey(Customer, 
                                on_delete=models.CASCADE,
                                related_name="owner",
                                null=True)
    price = models.DecimalField(_('A price'), default=0, max_digits=4,
                                decimal_places=2)
    image = models.ImageField(verbose_name=_('An image of the product'),
                              upload_to="products/")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True,
                                 blank=True)
    digital = models.BooleanField(default=False,null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def get_absolute_url(self):
        return '/products/'

    def __str__(self):
        return f'{self.name} {self.price}$'

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @property
    def set_default_slug(self):
        return slugify(f'{self.category or "products"}-{self.name}-{self.product_id}')

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        
        
class Category(models.Model):
    category_id = models.UUIDField("A Category id", primary_key=True, default=uuid.uuid4,
                                   editable=False)
    # category_id = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=100)
    name = models.CharField(max_length=30, null=False, blank=False)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


    def __str__(self):
        return self.name
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    @property
    def set_default_slug(self):
        return f'{self.name}'