from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import requests

from .utils import get_client_ip, save_request


def proxy_js(request):
    url = settings.MATOMO_BASE_URL + request.get_full_path()
    save_request(request)
    response = requests.get(url)
    return HttpResponse(response.content, status=response.status_code, content_type=response.headers['Content-Type'])


def proxy_php(request):
    url = settings.MATOMO_BASE_URL + request.get_full_path()
    url += '&token_auth=' + settings.MATOMO_TOKEN_AUTH
    url += '&cip=' + get_client_ip(request)
    headers = {
        'User-agent': request.META['HTTP_USER_AGENT'],
    }
    response = requests.get(url, headers=headers)
    return HttpResponse(response.content, status=response.status_code, content_type=response.headers['Content-Type'])


def check_tracking_js(request):
    context = {
        'matomo_site_id':   settings.MATOMO_SITE_ID,
        'ip':               get_client_ip(request),
        'is_secure':        request.is_secure(),
    }
    return render(request, 'matomo_monorail/check_tracking_js.html', context)


def check_tracking_no_js(request):
    context = {
        'ip':               get_client_ip(request),
        'is_secure':        request.is_secure(),
    }
    return render(request, 'matomo_monorail/check_tracking_no_js.html', context)
