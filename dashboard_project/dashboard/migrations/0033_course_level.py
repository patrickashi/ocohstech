# Generated by Django 5.0.6 on 2024-08-14 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0032_course_courseregistration'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('100lv', '100 Level'), ('200lv', '200 Level'), ('300lv', '300 Level')], default=1, max_length=6),
            preserve_default=False,
        ),
    ]
