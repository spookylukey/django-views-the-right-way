from django.urls import path

from . import views

urlpatterns = [
    path('special-offers/<slug:slug>/', views.special_offer_detail, name='special_offer_detail'),
]

app_name = 'delegation'
