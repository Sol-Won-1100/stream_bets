from datetime import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import UserChannel, CustomUser



class ActiveStreamBet(models.Model):
    """
    Активная ставка стримеров
    """
    CURRENT_EVENT_STATUS = (
        ('bets_accept', 'Приём ставок'),
        ('bets_made', 'Ставки сделаны'),
        ('bets_in_process', 'Идёт игра')
    )

    EVENT_BET_AMOUNT = (
        ('100', '100'),
        ('200', '200'),
        ('300', '400'),
        ('400', '400'),
        ('500', '500'),
        ('600', '600'),
        ('700', '700'),
        ('800', '800'),
        ('900', '900'),
        ('1000', '1000')
    )

    event_streamer = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='Стример')
    event_channel = models.OneToOneField(UserChannel,  on_delete=models.CASCADE, related_name='streamer_channel')
    enent_created = models.DateTimeField(auto_now_add=True)
    event_bet_amount = models.CharField(choices=EVENT_BET_AMOUNT, max_length=32, verbose_name='Сумма ставок', default = '100')
    event_opened_until = models.DateTimeField(blank=True, null=True)
    event_close_on = models.DateTimeField(blank=True, null=True)
    event_status = models.CharField(choices=CURRENT_EVENT_STATUS, max_length=32, verbose_name='Текущий статус стрима', null = True, blank = True)

    event_opened = models.BooleanField(default = True)
    event_made = models.BooleanField(default = False)
    event_process = models.BooleanField(default = False)


    def __str__(self):
        return self.event_channel.channel_url
    


class CurrentUserBet(models.Model):
    """Моделька хранит инфу о том, кто и на что поставил
    """
    BET_TYPE = (
        ('win', 'Победа'),
        ('lost', 'Поражение')
    )
    user_event_bet = models.ForeignKey(UserChannel, on_delete=models.CASCADE)  # Куда именно поставил юзер.
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bet_date = models.DateTimeField(auto_now_add = True)
    bet_amount = models.IntegerField(default = 0, verbose_name='Сумма ставки')
    streamer_name = models.CharField(max_length=32, default='')
    #event_result = models.CharField(default = 'Не ресчитано', max_length=32, verbose_name='Результат игры')
    user_bet_type = models.CharField(choices=BET_TYPE, max_length=32, verbose_name='На что поставил', null = True, blank = True)
    

    def __str__(self):
        return   str(self.user) + ' ' + 'Поставил на:' + ' ' + str(self.user_event_bet)


    class Meta:
        db_table = 'current_active_user_bets'


