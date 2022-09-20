from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Customer, Profile


@receiver(post_save, sender=Customer)
def create_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        print(user)
        Profile.objects.create(
            # username=user.username,
            # email=user.email,
            # # profile=user.profile,
            # password=user.password,
            # first_name=user.first_name,
            # last_name=user.last_name,
            # phone=user.phone,
            # featured_img = user.featured_img,
            # gender=user.gender
            user=user
            
        )
        
@receiver(pre_save, sender=Customer)
def update_profile(sender, instance, **kwargs):
    profile = instance
    if profile.customer_id is not None:
        Profile.objects.update(user=profile)
        

@receiver(post_delete, sender=Customer)
def delete_profile(sender, instance, **kwargs):
    user = instance
    customer = Customer.objects.filter(email=user.email).first()
    if user and customer:
        # profile.delete()
        customer.delete()
    