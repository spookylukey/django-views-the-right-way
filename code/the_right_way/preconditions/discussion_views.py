from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views.generic import TemplateView


class PremiumRequired1:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_premium:
            return HttpResponseRedirect(reverse('preconditions:account'))
        return super().dispatch(request, *args, **kwargs)


class GoodReputationRequired1:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.good_reputation:
            return HttpResponseRedirect(reverse('preconditions:account'))
        return super().dispatch(request, *args, **kwargs)


# This works - both tests are executed
class SpecialView1(PremiumRequired1, GoodReputationRequired1, TemplateView):
    template_name = "special.html"


class PremiumRequired2(UserPassesTestMixin):
    login_url = 'preconditions:account'

    def test_func(self):
        return self.request.user.is_premium


class GoodReputationRequired2(UserPassesTestMixin):
    login_url = 'preconditions:account'

    def test_func(self):
        return self.request.user.good_reputation


# This does not work! GoodReputationRequired2.test_func is skipped
class SpecialView2(PremiumRequired2, GoodReputationRequired2, TemplateView):
    template_name = "special.html"
