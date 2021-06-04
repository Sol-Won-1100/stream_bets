# Generated by Django 3.2.4 on 2021-06-04 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userchannel_is_channel_live'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userchannel',
            name='channel_url',
        ),
        migrations.AddField(
            model_name='userchannel',
            name='real_twitch_channel_name',
            field=models.CharField(default='twitch_channel', max_length=64, unique=True),
        ),
    ]