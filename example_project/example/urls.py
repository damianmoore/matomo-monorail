from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from matomo_monorail.views import check_tracking_js, check_tracking_no_js, proxy_js, proxy_php


urlpatterns = [
    path('admin/', admin.site.urls),
    path('matomo.js', proxy_js),
    path('matomo.php', proxy_php),
    path('no-js-tracking/', check_tracking_no_js),
    path('', check_tracking_js),
]
