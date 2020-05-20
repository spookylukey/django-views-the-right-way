from django.urls import path

from . import views

urlpatterns = [
    path('checkout/start/', views.checkout_start, name='checkout_start'),
]

app_name = 'common_context_data'
