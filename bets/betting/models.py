from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import UserChannel, CustomUser


class CurrentActiveBet(models.Model):
    """Моделька для хранения открытых/активных ставок
    Удаляется как только стример/админ закрывает событие
    """
    EVENT_RESULT = (
        ('win', 'Победа'),
        ('lost', 'Поражение'),
        ('canceled', 'Отменить')

    )
    CURRENT_EVENT_STATUS = (
        ('accept_bets', 'Приём ставок'),
        ('bets_are_made', 'Ставки сделаны')
    )

    EVENT_GAME = (
        ('DOTA2', 'DOTA 2'),
        ('CS:GO', 'CS:GO')
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
    
    event_streamer = models.OneToOneField(UserChannel, on_delete=models.CASCADE, verbose_name='Стример')
    event_open_date = models.DateTimeField(auto_now_add = True)  # когда была нажата кнопка "принимаем ставки"
    event_status = models.CharField(choices=CURRENT_EVENT_STATUS, max_length=32, verbose_name='Текущий статус')  #  
    event_game = models.CharField(choices=EVENT_GAME, max_length=32, verbose_name='Игра')
    event_result = models.CharField(choices=EVENT_RESULT, max_length=32, verbose_name='Результат игры', null = True, blank = True)
    event_bet_amount = models.CharField(choices=EVENT_BET_AMOUNT, max_length=32, verbose_name='Сумма ставок', default = '100')
    envent_finish_taking_bets_time = models.DateTimeField(blank = True, null = True)  # время когда заканчивается приём ставок
    event_close = models.BooleanField(default = False)  #  Закрыты ли ставки


    def __str__(self):
        return str(str(self.event_streamer)  + '|' + self.event_game)


    class Meta:
        db_table = 'current_bets'

   


class CurrentUserBet(models.Model):
    """Моделька хранит инфу о том, кто и на что поставил
    """
    BET_TYPE = (
        ('win', 'Победа'),
        ('lost', 'Поражение')
        
    )
    user_event_bet = models.ForeignKey(CurrentActiveBet, on_delete=models.CASCADE)  # Куда именно поставил юзер.
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bet_date = models.DateTimeField(auto_now_add = True)
    bet_amount = models.IntegerField(default = 0, verbose_name='Сумма ставки')
    event_result = models.CharField(default = 'Не ресчитано', max_length=32, verbose_name='Результат игры')
    user_bet_type = models.CharField(choices=BET_TYPE, max_length=32, verbose_name='На что поставил', null = True, blank = True)
    

    def __str__(self):
        return   str(self.user) + ' ' + 'Поставил на:' + ' ' + str(self.user_event_bet)


    class Meta:
        db_table = 'current_active_user_bets'