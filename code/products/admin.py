from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General',
         {'fields': ['name', 'slug', 'description']}
         ),
    ]


admin.site.register(Product, ProductAdmin)
