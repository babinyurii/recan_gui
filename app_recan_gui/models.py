from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Session)
def create_session_data(sender, instance, created, **kwargs):
    if created:
        SessionData.objects.create(session_key=instance)



def save_file(instance, filename):

    filename, file_ext = filename.rsplit('.', 1)

    return "{0}_{1}.{2}".format(filename, 
                                instance.session_key,
                                file_ext)


class SessionData(models.Model):
    session_key = models.OneToOneField(
        Session,
        on_delete=models.CASCADE
    )
    alignment = models.CharField(max_length=100, blank=True, null=True, verbose_name='alignment name')
    alignment_with_key = models.CharField(max_length=132, blank=True, null=True)
    align_len = models.IntegerField(blank=True, null=True, verbose_name='sequence length')
    region_start = models.IntegerField(default=0)
    region_end = models.IntegerField(blank=True, null=True)
    pot_rec_id = models.CharField(max_length=100, blank=True, null=True)
    pot_rec_index = models.IntegerField(default=0)
    window_size = models.IntegerField(default=50)
    window_shift = models.IntegerField(default=25)
    plot_div = models.TextField(null=True, blank=True, default="")
    dist_method = models.CharField(default='pdist', max_length=5, verbose_name='genetic distance method')
    align_file = models.FileField(upload_to=save_file, default=None, null=True)

    class Meta:
        verbose_name = "Uploaded alignment and its plotting settings"
        verbose_name_plural = "Uploaded alignments and their plotting settings"

