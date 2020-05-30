from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from shop.models import SpecialOffer
from .search import product_search, special_product_search, Filter


def product_list(request):
    return display_product_list(
        request,
        searcher=product_search,
        template_name='shop/product_list_unpaged.html',
    )


def special_offer_detail(request, slug):
    special_offer = get_object_or_404(SpecialOffer.objects.all(), slug=slug)

    def special_product_search_wrapper(filters, page=1):
        products = special_product_search(filters, special_offer, page=page)
        log_special_offer_product_view(request.user, special_offer, products)
        return products

    return display_product_list(
        request,
        context={
            'special_offer': special_offer,
        },
        searcher=special_product_search_wrapper,
        template_name='shop/special_offer_detail_unpaged.html',
    )


def display_product_list(request, *, context=None, searcher, template_name):
    if context is None:
        context = {}
    filters = collect_filtering_parameters(request)
    try:
        page = int(request.GET['page'])
    except (KeyError, ValueError):
        page = 1
    context['products'] = searcher(filters, page=page)
    return TemplateResponse(request, template_name, context)


FILTER_MAPPING = {
    'q': Filter.NAME,
    'color': Filter.COLOR,
}


def collect_filtering_parameters(request):
    filters = {}
    for query_key, filter_key in FILTER_MAPPING.items():
        val = request.GET.get(query_key, '').strip()
        if val:
            filters[filter_key] = val
    return filters


def log_special_offer_product_view(user, special_offer, products):
    print(user, special_offer, products)
