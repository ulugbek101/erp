from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _


class UserLoginView(LoginView):
    template_name = 'app_users/login.html'
    success_url = reverse_lazy('account')
    extra_context = {
        'title': _('Tizimga kirish')
    }


class UserAccountView(TemplateView):
    template_name = 'app_users/account.html'
