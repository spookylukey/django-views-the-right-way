from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('home-2/', views.home_2, name='home_2'),
]

app_name = 'context_data'
