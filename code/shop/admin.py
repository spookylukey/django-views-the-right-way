from django.contrib import admin

from .models import Product, SpecialOffer


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fieldsets = [
        ('General',
         {'fields': ['name', 'slug', 'description']}
         ),
    ]


class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


admin.site.register(Product, ProductAdmin)
admin.site.register(SpecialOffer, SpecialOfferAdmin)
