# Generated by Django 3.2.4 on 2021-06-05 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('betting', '0005_auto_20210605_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentactivebet',
            name='event_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='currentactivebet',
            name='event_status',
            field=models.CharField(choices=[('accept_bets', 'Приём ставок'), ('bets_are_made', 'Ставки сделаны'), ('bets_are_closed', 'Ставки не принимаются')], max_length=32, verbose_name='Текущий статус'),
        ),
    ]
