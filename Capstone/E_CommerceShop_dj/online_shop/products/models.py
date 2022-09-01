from django.db import models

import uuid  

from django.core import validators
from user_auth.models import Customer

class Product(models.Model):
    
    # product_id = models.UUIDField("A Product id",primary_key=True, default=uuid.uuid4,
    #                               editable=False)
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False, blank=False)
    description  = models.TextField(max_length=1000,blank=True, null=True)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.DecimalField('A price', default=0, max_digits=4,
                                decimal_places=2)
    image = models.ImageField(verbose_name='An image of the product',
                              upload_to="products/")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def get_absolute_url(self):
        return '/products/'

    def __repr__(self):
        return f'{self.id} {self.description} {self.price}'

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        
        
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False, blank=False)
    # category_id = models.UUIDField("A Category id", default=uuid.uuid4,
    #                                editable=False)
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
