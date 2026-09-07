import pytest
from django.contrib.auth import get_user_model

from apps.tickets.models import Category


@pytest.fixture
def category(db):
    return Category.objects.create(name="IT")


@pytest.fixture
def employee(db):
    return get_user_model().objects.create_user("emp", password="pass12345", role="employee")


@pytest.fixture
def agent(db):
    return get_user_model().objects.create_user("agent", password="pass12345", role="agent")
