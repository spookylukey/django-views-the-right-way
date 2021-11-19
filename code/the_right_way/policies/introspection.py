from importlib import import_module

from django.conf import settings
from django.contrib.admindocs.views import extract_views_from_urlpatterns


from .decorators import has_security_policy_applied


def check_policy_for_all_routes():
    errors = []
    urlconf = import_module(settings.ROOT_URLCONF)
    # extract_views_from_urlpatterns is an undocumented internal from the
    # contrib 'admindocs' module that happens to be useful for demo purposes.
    for (func, regex, namespace, name) in extract_views_from_urlpatterns(urlconf.urlpatterns):
        if not regex.startswith('policies/'):
            continue
        if not has_security_policy_applied(func):
            errors.append(
                (f"{func.__module__}.{func.__name__} needs to have a security policy applied",
                 regex),
            )
    return errors
