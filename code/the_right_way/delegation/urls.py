from django.urls import path

from . import views

urlpatterns = [
    path('special-offers/<slug:slug>/', views.special_offer_detail, name='special_offer_detail'),
    path('products/', views.product_list, name='product_list'),
]

app_name = 'delegation'
