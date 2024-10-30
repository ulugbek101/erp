from django.contrib.auth.models import UserManager



class UserModelManager(UserManager):
    def create_user(self, username, first_name, last_name, email=None, password=None):
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_student=True,
            is_teacher=False,
            is_admin=False,
        )

        if email:
            user.email = self.normalize_email(email=email)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password, email=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        user.is_student=False
        user.is_teacher=True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class StudentManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_student=True)


class TeacherManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=True)


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)
