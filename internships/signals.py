from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import InternshipApplication, Notification

@receiver(post_save, sender=InternshipApplication)
def create_notification_for_new_applicant(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(message=f"A new applicant,  {instance}  has applied.")
@receiver(post_delete, sender=InternshipApplication)
def create_notification_for_deleted_applicant(sender, instance, **kwargs):
    Notification.objects.create(message=f"application for {instance }  has been deleted.")
