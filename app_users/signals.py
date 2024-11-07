from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from app_users.models import Group, Subject, Teacher

User = get_user_model()


@receiver(pre_delete, sender=Subject)
def preserve_subject_name(sender, instance, **kwargs):
    group = Group.objects.get(subject=instance)
    group.subject_name = instance.name
    group.save()


@receiver(pre_delete, sender=Teacher)
def preserve_teacher_name(sender, instance, **kwargs):
    group = Group.objects.get(teacher=instance)
    group.teacher_name = instance.fullname
    group.save()


@receiver(pre_delete, sender=Group)
def set_group_name_on_group_delete(sender, instance, **kwargs):
    user = User.objects.get(student_group=instance)
    user.student_group_name = instance.name
    user.save()

    for lesson in instance.lesson_set.all():
        lesson.group_name = instance.name
        lesson.save()
