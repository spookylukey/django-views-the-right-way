from django.urls import path

from . import views

urlpatterns = [
    path('products/<slug:product_slug>/', views.product_detail, name='product_detail'),
]

app_name = 'url_parameters'
