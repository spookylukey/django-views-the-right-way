# For more information please see:
#     https://docs.djangoproject.com/en/3.0/topics/http/urls/
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('view-source/<str:namespace>/', views.view_source, name='view_source'),
    path('admin/', admin.site.urls),
    path('the-pattern/', include('the_right_way.the_pattern.urls')),
    path('the-pattern-explanation/', include('the_right_way.the_pattern.explanation_urls')),
    path('context-data/', include('the_right_way.context_data.urls')),
    path('context-data-discussion/', include('the_right_way.context_data.discussion_urls')),
    path('common-context-data/', include('the_right_way.common_context_data.urls')),
    path('common-context-data-discussion/', include('the_right_way.common_context_data.discussion_urls')),
    path('url-parameters/', include('the_right_way.url_parameters.urls')),
    path('url-parameters-discussion/', include('the_right_way.url_parameters.discussion_urls')),
    path('detail-view/', include('the_right_way.detail_view.urls')),
    path('detail-view-discussion/', include('the_right_way.detail_view.discussion_urls')),
    path('list-view/', include('the_right_way.list_view.urls')),
    path('list-view-discussion/', include('the_right_way.list_view.discussion_urls')),
]
