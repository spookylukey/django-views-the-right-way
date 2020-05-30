from django.contrib import admin

from .models import Color, Product, SpecialOffer


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fieldsets = [
        ('General',
         {'fields': ['name', 'slug', 'description', 'colors']}
         ),
    ]
    filter_horizontal = ['colors']


class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'rgb']


admin.site.register(Product, ProductAdmin)
admin.site.register(SpecialOffer, SpecialOfferAdmin)
admin.site.register(Color, ColorAdmin)
