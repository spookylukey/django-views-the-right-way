from datetime import date

from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.urls import get_resolver, get_urlconf


def index(request):
    return TemplateResponse(request, 'index.html', {'today': date.today()})


def view_source(request, namespace):
    module = views_module(namespace)
    if not module:
        raise Http404()
    return HttpResponse(
        open(module.__file__).read(),
        content_type='text/plain',
    )


def views_module(namespace):
    urlconf = get_urlconf()
    resolver = get_resolver(urlconf)
    _, sub_resolver = resolver.namespace_dict[namespace]
    if hasattr(sub_resolver.urlconf_module, 'views'):
        return sub_resolver.urlconf_module.views
    return None
