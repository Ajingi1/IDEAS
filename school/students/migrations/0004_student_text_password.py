# Generated by Django 5.1 on 2024-09-03 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_customuser_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='text_password',
            field=models.TextField(blank=True),
        ),
    ]
