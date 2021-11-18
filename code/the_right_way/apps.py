from django.apps import AppConfig
from django.core.checks import Error, Tags, register

from the_right_way.policies.introspection import check_policy_for_all_routes


class TheRightWayConfig(AppConfig):
    name = "the_right_way"

    def ready(self):
        check_policy_for_all_routes()


@register(Tags.urls)
def check_view_policy(app_configs, **kwargs):
    return [
        Error(message, obj=url_pattern, id="the_right_way.TRW01")
        for message, url_pattern in check_policy_for_all_routes()
    ]
