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
    alignment = models.CharField(max_length=100, blank=True, null=True)
    alignment_with_key = models.CharField(max_length=150, blank=True, null=True)
    align_len = models.IntegerField(blank=True, null=True)
    region_start = models.IntegerField(default=0)
    region_end = models.IntegerField(blank=True, null=True)
    pot_rec_id = models.CharField(max_length=50, blank=True, null=True)
    pot_rec_index = models.IntegerField(default=0)