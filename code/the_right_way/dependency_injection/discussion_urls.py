from django.urls import path

from . import discussion_views as views


urlpatterns = [
    path('special-offers/<slug:slug>/', views.SpecialOfferDetail.as_view(), name='special_offer_detail'),
    path('products/', views.ProductList.as_view(), name='product_list'),
]

app_name = 'dependency_injection_discussion'
