# Generated by Django 5.1.3 on 2024-11-26 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0039_alter_course_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='faculty',
        ),
    ]