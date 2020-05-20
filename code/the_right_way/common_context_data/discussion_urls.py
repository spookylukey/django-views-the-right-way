from django.urls import path

from . import discussion_views as views

urlpatterns = [
    path('checkout/start/', views.CheckoutStart.as_view(), name='checkout_start'),
]

app_name = 'common_context_data_discussion'
