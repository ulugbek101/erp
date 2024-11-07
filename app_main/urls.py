from django.urls import path

from . import views

urlpatterns = [
    path("", views.redirect_to_home),
    path("teacher-groups/", views.TeacherGroups.as_view(), name="teacher_groups"),
    path("teacher-groups/<str:pk>/", views.TeacherGroupDetail.as_view(), name="teacher_group_detail"),
]
