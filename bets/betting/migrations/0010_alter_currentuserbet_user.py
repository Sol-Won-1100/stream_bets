# Generated by Django 3.2.4 on 2021-06-05 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('betting', '0009_auto_20210605_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentuserbet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
