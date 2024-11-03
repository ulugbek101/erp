from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.contrib import messages

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

    def form_invalid(self, form):
        messages.error(self.request, _("Login yoki Parol noto'g'ri terildi"))
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        messages.info(self.request, f"{_('Xush kelibsiz')}, {self.request.user.fullname} 👋")
        return super().get_success_url()


class UserLogourView(LogoutView):
    def post(self, request, *args, **kwargs):
        messages.info(request, _('Tizimdan muvaffaqiyatli chiqdingiz'))
        return super().post(request, *args, **kwargs)


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
            messages.success(request, _("Parol muvaffaqiyatli o'zgartirildi"))
            return redirect("account")
        else:
            # TODO: Pre-fill the password fields and open modal window for user
            messages.error(request, _("Parollar bir xil bo'lishi shart"))
            return redirect("account")
    else:
        messages.error(request, _("Ikkala parol sohasi ham kerak bo'ladi"))
        return redirect("account")


def update_account_username(request):
    username = request.POST.get("username")

    if username and len(username.strip()) > 0:
        user = request.user
        user.username = username
        user.save()
        messages.success(request, _("Username muvaffaqiyatli o'zgartirildi"))
        return redirect("account")
    else:
        # TODO: Pre-fill the username field and open modal window for user
        messages.warning(request, _("Username sohasi eng kamida 1 ta belgiga ega bo'lishi kerak"))
        return redirect("account")
