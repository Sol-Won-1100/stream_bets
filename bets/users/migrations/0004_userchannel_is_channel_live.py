# Generated by Django 3.2.4 on 2021-06-04 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userchannel'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchannel',
            name='is_channel_live',
            field=models.BooleanField(default=False),
        ),
    ]
