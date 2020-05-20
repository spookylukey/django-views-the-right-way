from django.urls import path

from . import other_views as views

urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    path('hello2/<str:my_arg>/', views.hello_world_2),
    path('hello3/<str:my_arg>/', views.hello_world_3),
    path('hello4/<str:my_arg>/', views.hello_world_4),
    path('hello5/<str:my_arg>/', views.hello_world_5),
]

app_name = 'the_pattern_other'
