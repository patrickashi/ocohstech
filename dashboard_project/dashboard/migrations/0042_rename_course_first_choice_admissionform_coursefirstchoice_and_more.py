# Generated by Django 5.1.3 on 2024-11-30 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0041_admissionform'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admissionform',
            old_name='course_first_choice',
            new_name='courseFirstChoice',
        ),
        migrations.RenameField(
            model_name='admissionform',
            old_name='course_second_choice',
            new_name='courseSecondChoice',
        ),
        migrations.RenameField(
            model_name='admissionform',
            old_name='guardians_phone_number',
            new_name='guardiansPhoneNumber',
        ),
        migrations.RenameField(
            model_name='admissionform',
            old_name='phone_number',
            new_name='phoneNumber',
        ),
    ]
