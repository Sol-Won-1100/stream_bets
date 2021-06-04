
from users.models import CustomUser


def get_main_data(current_user_id):
    userdata = CustomUser.objects.get(id = current_user_id)
    return {
        "user_balance" : userdata.balance, 'total_win': userdata.total_win, 'total_lose': userdata.total_lose,
        'total_coin_earn': userdata.total_earn, 'custom_username': userdata.custom_username, 'avatar': userdata.avatar
    }