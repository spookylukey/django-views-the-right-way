from django.urls import path

from . import discussion_views as views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
]

app_name = 'context_data_discussion'
