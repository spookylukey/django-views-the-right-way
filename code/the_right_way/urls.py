# For more information please see:
#     https://docs.djangoproject.com/en/3.0/topics/http/urls/
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('the-pattern/', include('the_right_way.the_pattern.urls')),
    path('the-pattern-other/', include('the_right_way.the_pattern.other_urls')),
]
