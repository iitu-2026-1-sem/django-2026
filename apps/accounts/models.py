from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь Service Desk с ролью. Роль решает, что человек видит и может (RBAC — тема недели 5)."""

    class Role(models.TextChoices):
        EMPLOYEE = "employee", "Сотрудник"
        AGENT = "agent", "Исполнитель"
        MANAGER = "manager", "Руководитель"

    role = models.CharField("Роль", max_length=16, choices=Role.choices, default=Role.EMPLOYEE)
    department = models.CharField("Подразделение", max_length=120, blank=True)

    @property
    def is_agent(self) -> bool:
        return self.role in (self.Role.AGENT, self.Role.MANAGER)

    @property
    def is_manager(self) -> bool:
        return self.role == self.Role.MANAGER

    def __str__(self) -> str:
        return self.get_full_name() or self.username
