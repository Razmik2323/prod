from time import time

from django.http import HttpRequest, HttpResponse


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_time = {}

    def __call__(self, request: HttpRequest):
        time_delay = 5
        ip = request.META['REMOTE_ADDR']
        if str(ip) in self.request_time:
            if self.request_time[str(ip)] + time_delay > int(round(time(), 0)):
                return HttpResponse(f'<h1>Ошибка!</h1>'
                                    f'<h2>Вы не можете отправлять запросы чаще, чем раз в {time_delay} секунд.</h2>')
        self.request_time = {str(ip): int(round(time(), 0))}

        response = self.get_response(request)

        return response


