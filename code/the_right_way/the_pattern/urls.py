from django.urls import path

from . import views

urlpatterns = [
    path('example/<str:arg>/', views.example_view, name='example_name'),
]

app_name = 'the_pattern'
