from django.urls import path

from . import decorator_include_views as views

urlpatterns = [
    path('my-premium-page/', views.my_premium_page, name='my_premium_page'),
]
