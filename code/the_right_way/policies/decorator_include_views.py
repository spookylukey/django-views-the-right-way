from django.template.response import TemplateResponse


def my_premium_page(request):
    return TemplateResponse(request, 'premium_page.html', {})
