# Generated by Django 3.2.4 on 2021-06-04 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betting', '0002_currentactivebet_event_bet_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentactivebet',
            name='event_game',
            field=models.CharField(choices=[('DOTA2', 'DOTA 2'), ('CS:GO', 'CS:GO')], max_length=32, verbose_name='Игра'),
        ),
    ]
