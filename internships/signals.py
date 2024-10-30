from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import InternshipApplication, Notification

@receiver(post_save, sender=InternshipApplication)
def create_notification_for_new_applicant(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(message="A new applicant has applied.")
@receiver(post_delete, sender=InternshipApplication)
def create_notification_for_deleted_applicant(sender, instance, **kwargs):
    Notification.objects.create(message="An applicant's application has been deleted.")
