# Generated by Django 2.0.4 on 2018-08-20 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_torrent_download_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
