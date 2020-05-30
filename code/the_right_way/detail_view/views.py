from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from shop.models import Product


def product_detail(request, slug):
    return TemplateResponse(request, 'shop/product_detail.html', {
        'product': get_object_or_404(Product.objects.all(), slug=slug),
    })


# Version without the shortcut:
def product_detail_longer(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        raise Http404
    return TemplateResponse(request, 'shop/product_detail.html', {
        'product': product,
    })
