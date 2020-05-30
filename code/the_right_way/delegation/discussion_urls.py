from django.urls import path

from . import discussion_views as views

urlpatterns = [
    path('special-offers-fbv/<slug:slug>/', views.special_offer_detail, name='special_offer_detail_fbv'),
    path('special-offers-cbv/<slug:slug>/', views.SpecialOfferDetail.as_view(), name='special_offer_detail_cbv'),
]

app_name = 'delegation_discussion'
