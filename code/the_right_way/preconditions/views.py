import functools
from django.template.response import TemplateResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required


def premium_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_premium:
            messages.info(request, "You need a premium account to access that page.")
            return HttpResponseRedirect(reverse('preconditions:account'))
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@premium_required
def my_premium_page(request):
    return TemplateResponse(request, 'premium_page.html', {})


def my_premium_page_longhand(request):
    return TemplateResponse(request, 'premium_page.html', {})


my_premium_page_longhand = \
    login_required(
        premium_required(
            my_premium_page_longhand
        )
    )


def my_premium_page_original(request):
    if not request.user.is_premium:
        messages.info(request, "You need a premium account to access that page.")
        return HttpResponseRedirect(reverse('preconditions:account'))
    return TemplateResponse(request, 'premium_page.html', {})


@login_required
def account(request):
    return TemplateResponse(request, 'account.html', {'user': request.user})
