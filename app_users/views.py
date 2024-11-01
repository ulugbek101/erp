from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .forms import UserAuthenticationForm


class UserLoginView(LoginView):
    template_name = "app_users/login.html"
    form_class = UserAuthenticationForm
    success_url = reverse_lazy("account")
    extra_context = {"title": _("Tizimga kirish")}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("account")
        return super().get(request, *args, **kwargs)


class UserAccountView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    template_name = "app_users/account.html"
    extra_context = {
        "account": True,
    }


def update_account_password(request):
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")

    if password1 and password2:
        if password1 == password2:
            user = request.user
            user.set_password(password2)
            login(request, user)
            user.save()
            # success message: Password changed
            return redirect("account")
        else:
            # TODO: Pre-fill the password fields and open modal window for user
            # error message: Passwords don't match
            return redirect("account")
    else:
        # error message: Both password fields required
        return redirect("account")


def update_account_username(request):
    username = request.POST.get("username")

    if username and len(username.strip()) > 0:
        user = request.user
        user.username = username
        user.save()
        # success message: Username changed
        return redirect("account")
    else:
        # TODO: Pre-fill the username field and open modal window for user
        # error message: Username length should at least one
        return redirect("account")


