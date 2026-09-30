from urllib.parse import urlsplit

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.canonical_url = urlsplit(settings.SITE_URL)
        self.canonical_host = self.canonical_url.netloc.lower()

    def __call__(self, request):
        request_host = request.get_host().split(':', 1)[0].lower()
        if request_host == 'ants.ac.ug':
            destination = f'{self.canonical_url.scheme}://{self.canonical_host}{request.get_full_path()}'
            return HttpResponsePermanentRedirect(destination)
        return self.get_response(request)