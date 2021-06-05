from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import UserChannel, CustomUser




   


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