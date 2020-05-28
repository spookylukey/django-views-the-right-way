from django.urls import path

from . import views

urlpatterns = [
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
]

app_name = 'detail_view'
