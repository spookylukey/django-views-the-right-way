import functools
from django.contrib import messages
from django.http import HttpResponseRedirect


_SECURITY_POLICY_APPLIED = "SECURITY_POLICY_APPLIED"


def premium_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_premium):
            messages.info(request, "You need to be logged in to a premium account to access that page.")
            return HttpResponseRedirect('/')
        return view_func(request, *args, **kwargs)

    setattr(wrapper, _SECURITY_POLICY_APPLIED, True)
    return wrapper


def anonymous_allowed(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    setattr(wrapper, _SECURITY_POLICY_APPLIED, True)
    return wrapper


def has_security_policy_applied(view_func):
    return getattr(view_func, _SECURITY_POLICY_APPLIED, False)


def check_security_policy_applied(view_func):
    if not has_security_policy_applied(view_func):
        raise AssertionError(f"{view_func.__module__}.{view_func.__name__} needs to have a security policy applied")
    return view_func
