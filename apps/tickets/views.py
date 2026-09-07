from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import TicketForm
from .models import Ticket


class TicketListView(LoginRequiredMixin, ListView):
    """Сотрудник видит свои заявки, исполнитель/руководитель — все (RBAC растёт в неделе 5)."""

    model = Ticket
    paginate_by = 20
    template_name = "tickets/list.html"

    def get_queryset(self) -> QuerySet[Ticket]:
        qs = Ticket.objects.select_related("category", "author", "assignee")
        if not self.request.user.is_agent:
            qs = qs.filter(author=self.request.user)
        status = self.request.GET.get("status")
        if status in Ticket.Status.values:
            qs = qs.filter(status=status)
        return qs


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "tickets/detail.html"

    def get_queryset(self) -> QuerySet[Ticket]:
        qs = Ticket.objects.select_related("category", "author", "assignee")
        return qs if self.request.user.is_agent else qs.filter(author=self.request.user)


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/form.html"
    success_url = reverse_lazy("tickets:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
