from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout", views.UserLogourView.as_view(), name="logout"),
    path("account/", views.UserAccountView.as_view(), name="account"),

    path("update-account-password/", views.update_account_password, name="update_account_password"),
    path("update-account-username/", views.update_account_username, name="update_account_username"),
]
