from django.template.response import TemplateResponse


def product_detail(request, slug):
    return TemplateResponse(request, 'shop/product_detail.html', {})
