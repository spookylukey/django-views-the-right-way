from django.views.generic import DetailView

from shop.models import Product


class ProductDetailView(DetailView):
    template_name = 'shop/product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'
