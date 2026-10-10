import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Category, Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    fields = ("title", "status", "author", "assignee", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "ticket_count")
    search_fields = ("name",)
    inlines = (TicketInline,)

    @admin.display(description="Количество заявок")
    def ticket_count(self, obj):
        return obj.tickets.count()


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "status",
        "author",
        "assignee",
        "created_at",
        "days_open",
    )

    list_filter = ("status", "created_at", "category")
    search_fields = (
        "title",
        "description",
        "author__username",
        "author__first_name",
        "author__last_name",
        "assignee__username",
        "assignee__first_name",
        "assignee__last_name",
    )

    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("category", "author", "assignee")
    date_hierarchy = "created_at"
    actions = ("close_selected_tickets", "assign_to_me", "export_to_csv")

    @admin.display(description="Дней с момента создания")
    def days_open(self, obj):
        from django.utils import timezone

        return (timezone.now() - obj.created_at).days

    @admin.action(description="Закрыть выбранные заявки")
    def close_selected_tickets(self, request, queryset):
        updated = queryset.exclude(
            status__in=(Ticket.Status.DONE, Ticket.Status.REJECTED)
        ).update(status=Ticket.Status.DONE)

        self.message_user(request, f"Закрыто заявок: {updated}.")

    @admin.action(description="Назначить себя исполнителем")
    def assign_to_me(self, request, queryset):
        updated = queryset.update(assignee=request.user)
        self.message_user(request, f"Назначено заявок: {updated}.")

    @admin.action(description="Экспортировать выбранные заявки в CSV")
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="tickets.csv"'
        response.write("\ufeff")

        writer = csv.writer(response)
        writer.writerow(
            ["ID", "Тема", "Описание", "Категория", "Статус",
             "Автор", "Исполнитель", "Дата создания"]
        )

        for ticket in queryset.select_related("category", "author", "assignee"):
            writer.writerow([
                ticket.pk,
                ticket.title,
                ticket.description,
                ticket.category.name,
                ticket.get_status_display(),
                ticket.author.get_username(),
                ticket.assignee.get_username() if ticket.assignee else "",
                ticket.created_at.strftime("%Y-%m-%d %H:%M"),
            ])

        return response

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        return queryset.filter(
            author=request.user
        ) | queryset.filter(assignee=request.user)

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_staff
