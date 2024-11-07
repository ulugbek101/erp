import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import PhoneNumberFormat, format_number, parse

from app_main.models import Subject

from .managers import AdminManager, StudentManager, TeacherManager
from .managers import UserModelManager as UserManager


class User(AbstractUser):
    class UserTypes(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Ustoz"
        ADMIN = "ADMIN", "Admin"
        SUPERUSER = "SUPERUSER", "Superadmin"

    username = models.CharField(verbose_name=_("Username"), max_length=50, unique=True)
    first_name = models.CharField(verbose_name=_("First name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last name"), max_length=50)
    profile_image = models.ImageField(
        verbose_name=_("Profile image"),
        upload_to="profile-images/",
        default="profile-images/user-default.png",
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name=_("Email"), max_length=50, null=True, blank=True
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Phone number"), null=True, blank=True
    )
    student_group = models.ForeignKey(
        verbose_name=_("Guruhi"),
        to="Group",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    student_group_name = models.CharField(
        verbose_name=_("Guruhi"), max_length=100, blank=True, null=True
    )
    is_studying = models.BooleanField(default=False)

    role = models.CharField(
        verbose_name=_("Role"),
        max_length=10,
        choices=UserTypes.choices,
        default=UserTypes.STUDENT,
    )

    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_phone_number(self):
        parsed_number = parse(str(self.phone_number), None)
        return format_number(parsed_number, PhoneNumberFormat.INTERNATIONAL)

    @property
    def fullname(self):
        return self.__str__()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.role or self.role is None:
            self.role = User.UserTypes.STUDENT

        if not self.password.startswith(("pbkdf2_", "argon2$", "bcrypt$", "sha1$")):
            self.set_password(self.password)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = ("first_name", "last_name")


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.role = User.UserTypes.STUDENT
        self.is_student = True
        self.is_teacher = False
        self.is_admin = False
        self.is_studying = True
        return super().save(*args, **kwargs)


class Teacher(User):
    class Meta:
        proxy = True

    objects = TeacherManager()

    def save(self, *args, **kwargs):
        self.type = User.UserTypes.TEACHER
        self.is_student = False
        self.is_teacher = True
        self.is_admin = False
        return super().save(*args, **kwargs)


class Admin(User):
    class Meta:
        proxy = True

    objects = AdminManager()

    def save(self, *args, **kwargs):
        self.type = User.UserTypes.ADMIN
        self.is_student = False
        self.is_teacher = False
        self.is_admin = True
        return super().save(*args, **kwargs)


class Group(models.Model):
    class LECTURE_DAYS_CHOICES(models.TextChoices):
        EVEN = "even", _("Dush, Chor, Jum")
        ODD = "odd", _("Sesh, Pay, Sha")
        BOOTCAMP = "bootcamp", _("Dush, Sesh, Chor, Pay, Jum")

    name = models.CharField(verbose_name=_("Guruh nomi"), max_length=100)
    subject = models.ForeignKey(
        to=Subject, verbose_name=_("Fan"), on_delete=models.SET_NULL, null=True
    )
    subject_name = models.CharField(
        verbose_name=_("Fan nomi"), max_length=50, blank=True
    )
    teacher = models.ForeignKey(
        "Teacher", verbose_name=_("Guruh ustozi"), on_delete=models.SET_NULL, null=True
    )
    teacher_name = models.CharField(
        verbose_name=_("Ustoz nomi"), max_length=100, blank=True
    )
    is_started = models.BooleanField(
        verbose_name=_("Boshlanganlik statusi"), default=True
    )
    start_date = models.DateField(verbose_name=_("Boshlanish sanasi"))
    end_date = models.DateField(verbose_name=_("Tugash sanasi"))
    lecture_days = models.CharField(
        verbose_name=_("Dars kunlari"),
        choices=LECTURE_DAYS_CHOICES.choices,
        max_length=26,
    )
    branch = models.CharField(verbose_name=_("Filial"), max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )

    @property
    def has_started(self):
        return self.is_started

    @property
    def has_ended(self):
        return self.end_date < timezone.now().date()

    @property
    def has_not_started(self):
        return self.start_date > timezone.now().date()

    def __str__(self):
        return f"{self.subject.name} {self.name}"


class Lesson(models.Model):
    theme = models.CharField(verbose_name=_("Mavzu"), max_length=200)
    start_time = models.TimeField(verbose_name=_("Boshlanish vaqti"))
    end_time = models.TimeField(verbose_name=_("Tugash vaqti"))
    group = models.ForeignKey(to=Group, verbose_name=_("Guruh"), on_delete=models.SET_NULL, null=True)
    group_name = models.CharField(verbose_name=_("Guruh"), max_length=100, blank=True, null=True)

    def __str__(self):
        return self.theme
