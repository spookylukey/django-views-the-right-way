from django.urls import path

from . import discussion_views as views

urlpatterns = [
    path('special-1/', views.SpecialView1.as_view(), name='special_1'),
    path('special-2/', views.SpecialView2.as_view(), name='special_2'),
]

app_name = 'preconditions_discussion'
