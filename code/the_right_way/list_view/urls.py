from django.urls import path

from . import views

urlpatterns = [
    path('products-unpaged/', views.product_list_unpaged, name='product_list_unpaged'),
    path('products/', views.product_list, name='product_list'),
    path('products-refactored/', views.product_list_refactored, name='product_list_refactored'),
]

app_name = 'list_view'
