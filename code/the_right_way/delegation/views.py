from django.template.response import TemplateResponse

from shop.models import SpecialOffer
from django.shortcuts import get_object_or_404


# TODO finish me
def special_offer_detail(request, slug):
    special_offer = get_object_or_404(SpecialOffer.objects.all(), slug=slug)
    return TemplateResponse(request, 'shop/special_offer_detail.html', {
        'special_offer': special_offer,
        'products': special_offer.get_products(),
    })
