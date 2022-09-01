from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Customer, Profile

@receiver(post_save, sender=Customer)
def create_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        Profile.objects.create(
            owner=user
        )
        #     first_name=user.first_name or None,
        #     last_name=user.last_name or None,
        #     username=user.username or None,
        #     phone=user.phone or None,
        #     email=user.email,
        #     password=user.password
        # )
@receiver(post_save, sender=Customer)
def update_profile(sender, instance, created, **kwargs):
    print(instance)
    profile = instance
    if created == False:
        Profile.objects.update(
            first_name=profile.first_name,
            last_name=profile.last_name,
            username=profile.username,
            email=profile.email,
            password=profile.password,
            phone=profile.phone,
            )