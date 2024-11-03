from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView

from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('account'))
]

urlpatterns += i18n_patterns(
    path('users/', include('app_users.urls')),
    path('', include('app_main.urls')),
    path('password-reset/', PasswordResetView.as_view(template_name='app_users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='app_users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='app_users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='app_users/password_reset_complete.html'), name='password_reset_complete'),
)

urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
