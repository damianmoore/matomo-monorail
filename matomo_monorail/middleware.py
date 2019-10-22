from django.conf import settings

from .utils import save_request


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Create DB object before the view (and later middleware) are called
        save_request(request)

        # Call middlewares that are next and return to those that are previous
        return self.get_response(request)
