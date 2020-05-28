from django.template.response import TemplateResponse


def product_detail(request, product_slug):
    return TemplateResponse(request, 'shop/product_detail.html', {})
