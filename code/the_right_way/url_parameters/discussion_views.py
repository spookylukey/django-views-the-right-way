from datetime import date

from django.http import HttpResponse
from django.template.response import TemplateResponse

# Example showing type hints, which are checked by ../url_checker.py
# Try changing the types here or in urls.py
#
# See also SILENCED_SYSTEM_CHECKS in settings.py


def product_detail_2(request, name: str):
    return TemplateResponse(request, 'shop/product_detail.html', {})


def product_detail_3(request, pk: int):
    return TemplateResponse(request, 'shop/product_detail.html', {})


# Example with custom converter - see DateConverter

def diary_entry(request, post_date: date):
    return HttpResponse(f'My diary on {post_date.strftime("%A, %e %B %Y")}')
