from django.urls import path

from . import discussion_views as views

urlpatterns = [
    path('products/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
]

app_name = 'detail_view_discussion'
