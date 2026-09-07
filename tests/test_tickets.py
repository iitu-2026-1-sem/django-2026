import pytest
from django.urls import reverse

from apps.tickets.models import Ticket


def test_health(client):
    r = client.get(reverse("health"))
    assert r.status_code == 200 and r.json()["ok"] is True


def test_list_requires_login(client):
    r = client.get(reverse("tickets:list"))
    assert r.status_code == 302 and "/login/" in r["Location"]


@pytest.mark.django_db
def test_employee_creates_and_sees_only_own(client, employee, agent, category):
    client.force_login(employee)
    r = client.post(
        reverse("tickets:create"), {"title": "Не работает принтер", "category": category.pk, "description": "3 этаж"}
    )
    assert r.status_code == 302
    t = Ticket.objects.get()
    assert t.author == employee and t.status == Ticket.Status.NEW
    Ticket.objects.create(title="чужая", description="x", category=category, author=agent)
    r = client.get(reverse("tickets:list"))
    assert list(r.context["object_list"]) == [t]


@pytest.mark.django_db
def test_agent_sees_all(client, employee, agent, category):
    Ticket.objects.create(title="a", description="x", category=category, author=employee)
    Ticket.objects.create(title="b", description="y", category=category, author=agent)
    client.force_login(agent)
    r = client.get(reverse("tickets:list"))
    assert r.context["object_list"].count() == 2
