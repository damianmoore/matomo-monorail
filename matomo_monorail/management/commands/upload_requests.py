import os
from datetime import datetime, timedelta
from time import sleep

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
import requests

from matomo_monorail.models import Request


SECONDS_TO_CONSOLIDATE = 10


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-d',
            action='store_true',
            dest='daemon',
            default=False,
            help='Run in daemon mode')

    def handle(self, *args, **options):
        if options['daemon']:
            self.sync_loop()
        else:
            self.sync_requests()

    def sync_loop(self):
        while True:
            self.sync_requests()
            sleep(60)

    def sync_requests(self):
        print('Syncing requests')

        if not settings.MATOMO_BASE_URL:
            print('settings.MATOMO_BASE_URL is not configured')
            exit(1)

        end_datetime = timezone.now() - timedelta(seconds=SECONDS_TO_CONSOLIDATE)
        for proxy_request in Request.objects.filter(type='S').filter(created__lte=end_datetime).order_by('created'):
            match = Request.objects.filter(type='C', url=proxy_request.url, ip=proxy_request.ip, user_agent=proxy_request.user_agent).order_by('created').first()

            if match:
                match.delete()
                proxy_request.delete()

            else:
                url = settings.MATOMO_BASE_URL + f'matomo.php?idsite={settings.MATOMO_SITE_ID}&'
                extra_params = [
                    'rec=1',
                    'url=' + proxy_request.url,
                    'apiv=1',
                    'urlref=' + proxy_request.referer,
                    'ua=' + proxy_request.user_agent,
                    f'cdt={int(proxy_request.created.timestamp())}',
                    'token_auth=' + settings.MATOMO_TOKEN_AUTH,
                    'cip=' + proxy_request.ip,
                ]
                url += '&'.join(extra_params)

                response = requests.get(url)

                if response.status_code == 200:
                    print('Success')
                    proxy_request.delete()
                else:
                    print('Failed to submit')
