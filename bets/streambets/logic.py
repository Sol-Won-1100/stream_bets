from datetime import date, datetime, timedelta
from django.utils import timezone
from django.db.models import F

from users.models import CustomUser, UserChannel
from .get_data import get_main_data
from betting.models import CurrentUserBet

def get_current_channel_info(uid, channel_url):
    channel_data = UserChannel.objects.get(channel_url = channel_url)
    data = {}
    data['bet_amount'] = channel_data.event_bet_amount
    data['streamer_name'] = channel_data.channel_url

    if channel_data.streamer.id == uid:
        data['is_admin'] = True
    else:
        data['is_viewer'] = True
        
    # Если событие не создано и юзер админ канала
    if channel_data.channel_status == 'bets_are_closed' and channel_data.streamer.id == uid:
        data['not_started'] = True
        #TODO: Устанавливать все данные в дефолт
        return data

    # Если открыт приём ставок
    if channel_data.channel_status == 'accept_bets':
        #TODO: проверять таймер 30 минут -> возврат ставок
        data['is_bet_opened'] = True
        # через сколько нужно закрыть приём и нажать "ставки сделаны"
        data['open_until'] = channel_data.event_finish_accepting_at.replace(microsecond=0) - datetime.now().replace(microsecond=0)
        return data
        
    #ставки сделаны
    if channel_data.channel_status == 'bets_are_made':
        data['bets_are_made'] = True
        if channel_data.event_close_bet_at > datetime.now(): # таймер живой
            # сколько осталось (не больше 3 минут)
            data['event_close_timer'] = channel_data.event_close_bet_at.replace(microsecond=0) - datetime.now().replace(microsecond=0)
            return data
        elif channel_data.event_close_bet_at < datetime.now(): # время вышло, закрываем ставку и стаим статус в процессе
            UserChannel.objects.filter(channel_url = channel_url).update(channel_status = 'bets_in_process')
            data['bet_in_process'] = True
            return data

    if channel_data.channel_status == 'bets_in_process':
        data['in_process'] = True
        #  Если событие в процессе - показывать таймер.
        data['event_finish_timer'] = channel_data.event_finish_at.replace(microsecond=0) - datetime.now().replace(microsecond=0)
        return data
    data['channel_url'] = channel_data.channel_url
    
    print("CURRENT DATA",data)
    return data
    

def update_current_channel_info(uid, channel):
    try:
        current_channel = UserChannel.objects.get(channel_url = channel)
        if current_channel.channel_status == 'accept_bets':
            # открыли приём ставок
            try:
                if current_channel.event_finish_accepting_at < datetime.now():
                    print('Вернули ставки')
            except TypeError:
                pass
        
        elif current_channel.channel_status == 'bets_are_made':
            #ставки сделаны
            if current_channel.event_close_bet_at < datetime.now():
                UserChannel.objects.filter(channel_url = channel).update(channel_status = 'bets_in_process')

        elif current_channel.channel_status == 'bets_in_process':
            #  В процессе
            if current_channel.event_finish_at < datetime.now():
                print('Стример не завершил событие, возвращаем ставки')
                UserChannel.objects.filter(channel_url = channel).update(channel_status = 'bets_are_closed')

    except UserChannel.DoesNotExist:
        return False
    

def create_bet(uid, bet_amount):
    try:
        current_channel = UserChannel.objects.get(streamer = uid)
        if current_channel.channel_status  == 'bets_are_closed':
            # Можно открыть ставки
            UserChannel.objects.filter(streamer = uid).update(channel_status = 'accept_bets', 
            event_finish_accepting_at = datetime.now() + timedelta(minutes=30), 
            event_finish_at = datetime.now() + timedelta(minutes=180),
            event_bet_amount = bet_amount)

            return True
            
    except UserChannel.DoesNotExist:
        return False

def start_event(uid, wait_sec):
    try:
        current_channel = UserChannel.objects.get(streamer = uid)
        if current_channel.channel_status  == 'accept_bets':
            # Можно открыть ставки
            UserChannel.objects.filter(streamer = uid).update(channel_status = 'bets_are_made', 
            event_finish_accepting_at = datetime.now() + timedelta(minutes=30), 
            event_close_bet_at = datetime.now() + timedelta(seconds=wait_sec)
            )

            return True
        else:
            return False 
    except UserChannel.DoesNotExist:
        return False


def user_do_bet(uid, bet_type, channel):
    """
    Работа со ставками пользователей
    """
    current_user_data = get_main_data(uid)
    try:
        current_channel_data = UserChannel.objects.get(channel_url = channel)
        if int(current_user_data['user_balance']) >= int(current_channel_data.event_bet_amount) and current_channel_data.event_close_bet_at > datetime.now():
            CurrentUserBet.objects.create(user_event_bet_id = current_channel_data.id, user_id = uid, bet_amount = current_channel_data.event_bet_amount,
            user_bet_type = bet_type)
            CustomUser.objects.filter(id = uid).update(balance = F('balance') - int(current_channel_data.event_bet_amount))
            return True
        else:
            return False
    except UserChannel.DoesNotExist:
        return False


def get_bet_stats(channel):
    """
    Текущая статистика по ставкам
    """
    
    try:
        current_channel_data = UserChannel.objects.get(channel_url = channel)
        #current_channel_data.id
        all_bets = CurrentUserBet.objects.filter(user_event_bet_id = current_channel_data.id)
        win_bet = 0
        lost_bet = 0
        for i in all_bets:
            if i.user_bet_type == 'win':
                win_bet += 1
            if i.user_bet_type == 'lost':
                lost_bet += 1
        print({'win_bet': win_bet, 'lost_bet': lost_bet, 'total_bet': all_bets.count()})

        return {'win_bet': win_bet, 'lost_bet': lost_bet, 'total_bet': all_bets.count()}
    except UserChannel.DoesNotExist:
        print('except')
        return False
    


   