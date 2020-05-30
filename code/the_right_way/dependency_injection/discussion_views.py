from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from shop.models import SpecialOffer

from .search import product_search as all_product_search, special_product_search, Filter


class ProductSearchBase(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filters = collect_filtering_parameters(self.request)
        try:
            page = int(self.request.GET['page'])
        except (KeyError, ValueError):
            page = 1
        context['products'] = self.product_search(filters, page=page)
        return context

    def product_search(self, filters, page=1):
        raise NotImplementedError()


class ProductList(ProductSearchBase):
    template_name = 'shop/product_list_unpaged.html'

    def product_search(self, filters, page=1):
        return all_product_search(filters, page=page)


class SpecialOfferDetail(ProductSearchBase):
    template_name = 'shop/special_offer_detail_unpaged.html'

    def get(self, request, *args, **kwargs):
        special_offer = get_object_or_404(SpecialOffer.objects.all(), slug=kwargs['slug'])
        self.special_offer = special_offer
        return super().get(request, **kwargs)

    def product_search(self, filters, page=1):
        products = special_product_search(filters, self.special_offer, page=page)
        log_special_offer_product_view(self.request.user, self.special_offer, products)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['special_offer'] = self.special_offer
        return context


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
