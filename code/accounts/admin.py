from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Address, User


class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('is_premium', 'good_reputation')}),
    )


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'short_name',
        'first_line',
        'post_code',
        'primary',
    ]


admin.site.register(User, MyUserAdmin)
admin.site.register(Address, AddressAdmin)
