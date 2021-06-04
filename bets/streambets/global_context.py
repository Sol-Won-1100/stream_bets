from users.models import UserChannel, CustomUser
#from django.utils.deprecation import MiddlewareMixin

def current_live_channel(request):      
    live_channels = UserChannel.objects.filter(is_channel_live = True)
    return {'live_channel':live_channels}
