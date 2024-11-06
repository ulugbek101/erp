from django.urls import path

from . import views

urlpatterns = [
    path('', views.redirect_to_home),
    path('teacher-groups/', views.teacher_groups, name='teacher-groups'),
]
