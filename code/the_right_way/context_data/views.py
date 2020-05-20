from datetime import date

from django.template.response import TemplateResponse


def home(request):
    return TemplateResponse(request, "home.html", {
        'today': date.today(),
    })


def home_2(request):
    today = date.today()
    context = {
        'today': today,
    }
    if today.weekday() == 0:
        context['special_message'] = 'Happy Monday!'
    return TemplateResponse(request, "home.html", context)
