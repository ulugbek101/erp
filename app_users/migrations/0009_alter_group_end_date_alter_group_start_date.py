# Generated by Django 5.1.2 on 2024-11-07 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0008_alter_group_branch_alter_group_end_date_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='end_date',
            field=models.DateField(verbose_name='Tugash sanasi'),
        ),
        migrations.AlterField(
            model_name='group',
            name='start_date',
            field=models.DateField(verbose_name='Boshlanish sanasi'),
        ),
    ]
