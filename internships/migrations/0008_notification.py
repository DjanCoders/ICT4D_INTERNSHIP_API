# Generated by Django 5.1.2 on 2024-10-30 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0007_descquestion_mcqquestion_remove_answer_question_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(verbose_name=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
