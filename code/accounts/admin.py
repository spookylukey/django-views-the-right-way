from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Address, User


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'short_name',
        'first_line',
        'post_code',
        'primary',
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
