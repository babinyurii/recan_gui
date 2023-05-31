from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Session)
def create_session_data(sender, instance, created, **kwargs):
    if created:
        SessionData.objects.create(session_key=instance)


class SessionData(models.Model):
    session_key = models.OneToOneField(
        Session,
        on_delete=models.CASCADE
    )
    file_name = models.CharField(max_length=100, blank=True, null=True)