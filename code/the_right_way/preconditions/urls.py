from django.urls import path

from . import views

urlpatterns = [
    path('account/', views.account, name='account'),
    path('my-premium-page/', views.my_premium_page, name='my_premium_page'),
]

app_name = 'preconditions'
