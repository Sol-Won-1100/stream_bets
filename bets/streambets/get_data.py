
from users.models import CustomUser, UserChannel


def get_main_data(current_user_id):
    userdata = CustomUser.objects.get(id = current_user_id)
    user_channel_data = False
    try:
        user_channel_data = UserChannel.objects.get(streamer_id = current_user_id)
    except:
        pass
    
    return {
        "user_balance" : userdata.balance, 'total_win': userdata.total_win, 'total_lose': userdata.total_lose,
        'total_coin_earn': userdata.total_earn, 'custom_username': userdata.custom_username, 'avatar': userdata.avatar,
         'total_earn': userdata.total_earn, 'total_bet':userdata.total_bet, 'is_streamer': userdata.is_streamer, 'user_channel_data': user_channel_data
    }