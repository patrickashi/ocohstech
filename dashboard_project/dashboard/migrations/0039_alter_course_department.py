# Generated by Django 5.1.3 on 2024-11-25 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0038_delete_artscourses_delete_commercialcourses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='department',
            field=models.CharField(choices=[('communityhealth', 'Communityhealth'), ('medlab', 'Medlab'), ('pharmacy', 'Pharmacy'), ('dot', 'Dot')], max_length=20),
        ),
    ]