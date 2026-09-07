from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (("Service Desk", {"fields": ("role", "department")}),)
    list_display = ("username", "get_full_name", "role", "department", "is_active")
    list_filter = ("role", "department", "is_active")
