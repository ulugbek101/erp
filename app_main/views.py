from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from app_users.models import Group


def redirect_to_home(request):
    return redirect("account")


class TeacherGroups(ListView):
    template_name = "app_main/teacher-groups.html"
    context_object_name = "teacher_groups"
    group_statuses = {
        "active": _("Faol"),
        "not-active": _("Boshlanmagan"),
        "ended": _("Tugagan"),
    }
    extra_context = {
        "groups": True,
    }

    def get_queryset(self) -> QuerySet[Group]:
        self.groups_status = self.request.GET.get("group-status", "active")
        self.search = self.request.GET.get("search", "")

        groups = self.request.user.group_set.filter(name__icontains=self.search)

        if self.groups_status == "active":
            groups = groups.filter(is_started=True)
        elif self.groups_status == "not-active":
            groups = groups.filter(start_date__gt=timezone.now().date())
        elif self.groups_status == "ended":
            groups = groups.filter(end_date__lt=timezone.now().date())

        return groups

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context["group_status"] = self.group_statuses.get(self.groups_status, _("Faol"))
        context["search"] = self.search
        return context


class TeacherGroupDetail(DetailView):
    model = Group
    template_name = "app_main/teacher-group-detail.html"
    context_object_name = "teacher_group"
    extra_context = {
        "groups": True,
    }

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
