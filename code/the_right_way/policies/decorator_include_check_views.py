from django.template.response import TemplateResponse
from .decorators import premium_required, anonymous_allowed


@premium_required
def my_premium_page(request):
    return TemplateResponse(request, 'premium_page.html', {})


@anonymous_allowed
def non_premium_page(request):
    return TemplateResponse(request, 'ordinary.html', {})
