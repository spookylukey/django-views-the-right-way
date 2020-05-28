from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.http import Http404


from shop.models import Product


def product_detail(request, product_slug):
    return TemplateResponse(request, 'shop/product_detail.html', {
        'product': get_object_or_404(Product.objects.all(), slug=product_slug),
    })


# Version without the shortcut:
def product_detail_longer(request, product_slug):
    try:
        product = Product.objects.get(slug=product_slug)
    except Product.DoesNotExist:
        raise Http404
    return TemplateResponse(request, 'shop/product_detail.html', {
        'product': product,
    })
