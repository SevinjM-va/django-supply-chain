from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Warehouse, Product, Stock


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("User type", {"fields": ("user_type",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("User type", {"fields": ("user_type",)}),
    )


admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(Stock)