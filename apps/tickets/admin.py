from django.contrib import admin

from .models import Category, Ticket


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "status", "author", "assignee", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title", "description")
    autocomplete_fields = ("category",)
    date_hierarchy = "created_at"
