from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Customer, Profile

import datetime

@receiver(post_save, sender=Customer)
def create_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        Profile.objects.create(
            username=user.username,
            email=user.email,
            profile=user.profile,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            featured_img = profile.featured_img
            
        )
        
@receiver(pre_save, sender=Profile)
def update_profile(sender, instance, **kwargs):
    print(instance)
    profile = instance
    if profile.profile_id is not None:
        Profile.objects.update(
            
            username=profile.username,
            email=profile.email,
            password=profile.password,
            first_name=profile.first_name,
            last_name=profile.last_name,
            phone=profile.phone,
            description=profile.description,
            featured_img = profile.featured_img,
            )