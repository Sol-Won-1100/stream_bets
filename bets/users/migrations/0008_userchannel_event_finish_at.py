# Generated by Django 3.2.4 on 2021-06-05 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210605_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchannel',
            name='event_finish_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]