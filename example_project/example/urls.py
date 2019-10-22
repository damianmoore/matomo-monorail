from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from matomo_monorail.views import proxy_js, proxy_php


urlpatterns = [
    path('admin/', admin.site.urls),
    path('matomo.js', proxy_js),
    path('matomo.php', proxy_php),
    path('no-js-tracking/', TemplateView.as_view(template_name='no_js_tracking.html')),
    path('', TemplateView.as_view(template_name='js_tracking.html')),
]
