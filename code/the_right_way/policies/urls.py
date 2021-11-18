from django.urls import path
from decorator_include import decorator_include

from . import decorators

app_name = "policies"


urlpatterns = [
    path(
        "decorator-include/",
        decorator_include(
            [decorators.premium_required],
            ("the_right_way.policies.decorator_include_urls", app_name),
            namespace="policies_decorator_include",
        ),
    ),
    path(
        "decorator-include-check/",
        decorator_include(
            [decorators.check_security_policy_applied],
            ("the_right_way.policies.decorator_include_check_urls", app_name),
            namespace="policies_decorator_include_check",
        ),
    ),

]
