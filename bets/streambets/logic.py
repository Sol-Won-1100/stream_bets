from datetime import date, datetime
from django.utils import timezone
import pytz
from users.models import UserChannel


def get_current_channel_info(uid, channel_url):
    channel_data = UserChannel.objects.get(channel_url = channel_url)
    data = {}
    if channel_data.streamer.id == uid:
        data['is_admin'] = True
    else:
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
        return data
    
    
        

    data['channel_url'] = channel_data.channel_url

    return data
    
    
   