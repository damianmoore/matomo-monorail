import re

from .models import Request


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def save_request(request):
    # Don't log requests just fetching the tracking JS file
    if 'matomo.js' in request.path:
        return

    if 'matomo.php' in request.path:
        # Log Matomo JS client Request
        type = 'C'
        url = request.GET.get('url')
    else:
        # Log server Request
        type = 'S'
        uri = request.path
        if request.is_secure():
            url = f'https://{request.get_host()}{uri}'
        else:
            url = f'http://{request.get_host()}{uri}'

    Request(
        type=type,
        method=request.method,
        url=url,
        ip=request.META['REMOTE_ADDR'],
        user_agent=request.META['HTTP_USER_AGENT'],
        referer=request.META.get('HTTP_REFERER', '')
    ).save()
