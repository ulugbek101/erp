from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import Admin, Student, Teacher

User = get_user_model()


admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Teacher)
