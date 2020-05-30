from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from shop.models import Product


def product_list_unpaged(request):
    return TemplateResponse(request, 'shop/product_list_unpaged.html', {
        'products': Product.objects.all(),
    })


def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 5)  # Show 25 products per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return TemplateResponse(request, 'shop/product_list.html', {
        'page_obj': page_obj,
    })


def product_list_refactored(request):
    products = Product.objects.all()
    context = {}
    context.update(paged_object_list_context(request, products, paginate_by=25))
    return TemplateResponse(request, 'shop/product_list.html', context)


def paged_object_list_context(request, products, *, paginate_by):
    paginator = Paginator(products, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'page_obj': page_obj,
    }
