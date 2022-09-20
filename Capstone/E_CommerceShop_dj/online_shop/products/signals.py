from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Product, Category
# @receiver(post_save, sender=Product)
# def create_product(sender, instance, created, **kwargs):
#     if created:
#         instance.slug = slugify(f'{instance.category}-{instance.name}')
#         instance.save()


# @receiver(pre_save, sender=Product)
# def update_product(sender, instance, created, **kwargs):
#     if not created:
#         instance.slug = slugify(f'{instance.category or "products"} {instance.name}')
#         instance.save()