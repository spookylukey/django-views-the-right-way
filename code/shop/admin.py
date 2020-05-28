from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fieldsets = [
        ('General',
         {'fields': ['name', 'slug', 'description']}
         ),
    ]


admin.site.register(Product, ProductAdmin)
