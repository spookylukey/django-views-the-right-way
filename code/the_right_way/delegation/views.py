from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from shop.models import Product, SpecialOffer


def product_list(request):
    return display_product_list(
        request,
        queryset=Product.objects.all(),
        template_name='shop/product_list.html',
    )


def special_offer_detail(request, slug):
    special_offer = get_object_or_404(SpecialOffer.objects.all(), slug=slug)
    return display_product_list(
        request,
        context={
            'special_offer': special_offer,
        },
        queryset=special_offer.get_products(),
        template_name='shop/special_offer_detail.html',
    )


def display_product_list(request, *, context=None, queryset, template_name):
    if context is None:
        context = {}
    queryset = apply_product_filtering(request, queryset)
    context.update(paged_object_list_context(request, queryset, paginate_by=5))
    return TemplateResponse(request, template_name, context)


def apply_product_filtering(request, queryset):
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(name__icontains=query)
    return queryset


def paged_object_list_context(request, products, *, paginate_by):
    paginator = Paginator(products, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'page_obj': page_obj,
    }
