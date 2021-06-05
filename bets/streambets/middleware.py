class ChannelInfoMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        print('we are in fist')
        
        response = self._get_response(request)
        print(request.user.id)
        print('after')
        return response