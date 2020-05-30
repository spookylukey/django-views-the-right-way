from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from shop.models import SpecialOffer


def special_offer_detail(request, slug):
    special_offer = get_object_or_404(SpecialOffer.objects.all(), slug=slug)
    paginator = Paginator(special_offer.products.all(), 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return TemplateResponse(request, 'shop/special_offer_detail.html', {
        'special_offer': special_offer,
        'page_obj': page_obj,
    })


class SpecialOfferDetail(SingleObjectMixin, ListView):
    paginate_by = 2
    template_name = "shop/special_offer_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=SpecialOffer.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['special_offer'] = self.object
        return context

    def get_queryset(self):
        return self.object.products.all()
