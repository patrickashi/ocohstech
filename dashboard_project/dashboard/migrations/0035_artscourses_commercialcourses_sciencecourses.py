# Generated by Django 5.0.6 on 2024-09-12 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0034_medicalcourses_remove_courseregistration_course_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtsCourses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=10)),
                ('semester', models.CharField(choices=[('first', 'First Semester'), ('second', 'Second Semester')], max_length=10)),
                ('level', models.CharField(choices=[('100lv', '100 Level'), ('200lv', '200 Level'), ('300lv', '300 Level')], max_length=10)),
                ('credit_load', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CommercialCourses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=10)),
                ('semester', models.CharField(choices=[('first', 'First Semester'), ('second', 'Second Semester')], max_length=10)),
                ('level', models.CharField(choices=[('100lv', '100 Level'), ('200lv', '200 Level'), ('300lv', '300 Level')], max_length=10)),
                ('credit_load', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ScienceCourses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=10)),
                ('semester', models.CharField(choices=[('first', 'First Semester'), ('second', 'Second Semester')], max_length=10)),
                ('level', models.CharField(choices=[('100lv', '100 Level'), ('200lv', '200 Level'), ('300lv', '300 Level')], max_length=10)),
                ('credit_load', models.PositiveIntegerField()),
            ],
        ),
    ]