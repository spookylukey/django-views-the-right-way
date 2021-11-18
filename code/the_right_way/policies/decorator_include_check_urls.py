from django.urls import path

from . import decorator_include_check_views as views

urlpatterns = [
    path('my-premium-page/', views.my_premium_page, name='my_premium_page'),
    path('ordinary-page/', views.non_premium_page, name='non_premium_page'),
]
