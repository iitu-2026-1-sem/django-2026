from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField("Название", max_length=80, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Ticket(models.Model):
    """Заявка сотрудника. Стартовая модель — студенты расширяют её фичами (приоритет, история, вложения, SLA…)."""

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        IN_PROGRESS = "in_progress", "В работе"
        DONE = "done", "Выполнена"
        REJECTED = "rejected", "Отклонена"

    title = models.CharField("Тема", max_length=200)
    description = models.TextField("Описание")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.PROTECT, related_name="tickets")
    status = models.CharField("Статус", max_length=16, choices=Status.choices, default=Status.NEW, db_index=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Автор", on_delete=models.PROTECT, related_name="tickets"
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Исполнитель",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "-created_at"])]

    def __str__(self) -> str:
        return f"#{self.pk} {self.title}"
