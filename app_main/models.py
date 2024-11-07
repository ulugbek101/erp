from django.db import models
from django.utils.translation import gettext_lazy as _


class Subject(models.Model):
    name = models.CharField(verbose_name="Fan nomi", max_length=50, unique=True)

    def __str__(self):
        return self.name
