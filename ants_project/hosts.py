from django.conf import settings
from django_hosts import host, patterns

host_patterns = patterns(
    '',
    # Main website
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'', settings.ROOT_URLCONF, name='default'),

    # Subdomains - mapping to specific apps
    host(r'admissions', 'admissions.urls', name='admissions'),
    # host(r'gallery', 'gallery.urls', name='gallery'), # Uncomment when these apps are ready
    # host(r'events', 'events.urls', name='events'),
    # host(r'chapel', 'chapel.urls', name='chapel'),
)