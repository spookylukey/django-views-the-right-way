from django.views.generic.base import TemplateView


class CheckoutPageMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_anonymous:
            context["user_addresses"] = list(user.addresses.order_by("primary", "first_line"))
        return context


class CheckoutStart(CheckoutPageMixin, TemplateView):
    template_name = "shop/checkout/start.html"
