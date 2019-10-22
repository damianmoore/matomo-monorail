from django.utils import timezone

from django.db import models


REQUEST_TYPE_CHOICES = (
    ('C', 'Client'),
    ('S', 'Server'),
)


class Request(models.Model):
    created = models.DateTimeField(blank=True)
    type = models.CharField(max_length=1, choices=REQUEST_TYPE_CHOICES)
    method = models.CharField(max_length=6)
    url = models.TextField(blank=True)
    ip = models.CharField(max_length=15, blank=True)
    user_agent = models.TextField(blank=True)
    referer = models.TextField(blank=True)

    def __str__(self):
        return f'{self.created} {self.type} {self.method} {self.url} {self.ip} {self.user_agent}'

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.created:
            self.created = now
        self.updated = now
        super(Request, self).save()
