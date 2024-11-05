from django.db.models.signals import post_save,post_delete,pre_save
from django.dispatch import receiver
from .models import InternshipApplication, Notification,Internship
from django.utils import timezone


@receiver(post_save, sender=InternshipApplication)
def create_notification_for_new_applicant(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(message=f"A new applicant,  {instance}  has applied.")
@receiver(post_delete, sender=InternshipApplication)
def create_notification_for_deleted_applicant(sender, instance, **kwargs):
    Notification.objects.create(message=f"application for {instance }  has been deleted.")
def set_internship_active_status():
    # Efficiently update all expired internships in a single query
    current_date = timezone.now().date()
    Internship.objects.filter(end_date__lt=current_date, is_active=True).update(is_active=False)


    