from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=CustomUser)
def update_profile_full_name(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()