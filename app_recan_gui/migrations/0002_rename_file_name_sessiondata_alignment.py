# Generated by Django 4.2.1 on 2023-06-01 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_recan_gui', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sessiondata',
            old_name='file_name',
            new_name='alignment',
        ),
    ]
