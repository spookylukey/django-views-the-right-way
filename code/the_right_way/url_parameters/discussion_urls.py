from datetime import date

from django.urls import path, register_converter

from . import discussion_views as views


class DateConverter:
    regex = r'\d{4}-\d{2}-\d{2}'

    @staticmethod
    def to_python(value) -> date:
        year, month, day = value.split('-')
        return date(int(year), int(month), int(day))

    @staticmethod
    def to_url(value: date):
        return value.strftime('%F')


register_converter(DateConverter, 'isodate')


urlpatterns = [
    path('products/pk/<path:name>/', views.product_detail_2, name='product_detail_2'),
    path('products/pk/<int:pk>/', views.product_detail_3, name='product_detail_3'),
    path('post/<isodate:post_date>/', views.diary_entry, name='diary_entry'),
]

app_name = 'url_parameters_discussion'
