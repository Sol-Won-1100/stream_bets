# Generated by Django 3.2.4 on 2021-06-04 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210604_1922'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userchannel',
            old_name='real_twitch_channel_name',
            new_name='channel_url',
        ),
    ]
