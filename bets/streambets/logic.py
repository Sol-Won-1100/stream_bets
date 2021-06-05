from datetime import date, datetime, timedelta
from django.utils import timezone
import pytz
from users.models import UserChannel


def get_current_channel_info(uid, channel_url):
    channel_data = UserChannel.objects.get(channel_url = channel_url)
    data = {}
    if channel_data.streamer.id == uid:
        data['is_admin'] = True
    else:
        data['is_viewer'] = True
        return False
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

    return data
    

def update_current_channel_info(uid, channel):
    try:
        current_channel = UserChannel.objects.get(channel_url = channel)
        if current_channel.channel_status == 'accept_bets':
            # открыли приём ставок
            
            if current_channel.event_finish_accepting_at < datetime.now():
                print('Вернули ставки')
        
        elif current_channel.channel_status == 'bets_are_made':
            #ставки сделаны
            if current_channel.event_close_bet_at < datetime.now():
                UserChannel.objects.filter(channel_url = channel).update(channel_status = 'bets_in_process')

        elif current_channel.channel_status == 'bets_in_process':
            #  В процессе
            if current_channel.event_finish_at < datetime.now():
                print('Стример не завершил событие, возвращаем ставки')

    except UserChannel.DoesNotExist:
        return False
    

def create_bet(uid, bet_amount):
    try:
        current_channel = UserChannel.objects.get(streamer = uid)
        if current_channel.channel_status  == 'bets_are_closed':
            # Можно открыть ставки
            UserChannel.objects.filter(streamer = uid).update(channel_status = 'accept_bets', 
            event_finish_accepting_at = datetime.now() + timedelta(minutes=30), 
            event_finish_at = datetime.now() + timedelta(minutes=180))

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

   