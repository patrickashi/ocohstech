# Generated by Django 5.0.6 on 2024-05-16 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_student_user_id_student_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics'),
        ),
    ]
