from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_streamer = models.BooleanField(default= False)
    balance = models.IntegerField(default = 100, verbose_name='Текущий баланс')
    total_win = models.IntegerField(default = 0, verbose_name='Всего побед')
    total_lose = models.IntegerField(default = 0, verbose_name='Всего Поражений')
    total_earn = models.IntegerField(default = 0, verbose_name='Всего Заработано')
    custom_username = models.CharField(max_length=32, default = 'User Name', verbose_name="Никнейм")
    avatar = models.ImageField(upload_to='avatars', default = "avatars/default.png")
    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    objects = CustomUserManager()


    def __str__(self):
        return self.email


    class Meta:
        db_table = 'user_data'


class BetHistory(models.Model):
    """
    Храним статистику ставок пользователя
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    streamer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bet_on')
    bet_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default = False)
    bet_amount = models.PositiveIntegerField(default = 1)
    win_amount = models.IntegerField(default = 0)

    class Meta:
        db_table = 'user_bets'