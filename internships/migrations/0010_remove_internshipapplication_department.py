# Generated by Django 5.1.2 on 2024-10-31 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0009_internshipapplication_applly_for_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internshipapplication',
            name='department',
        ),
    ]
