# Generated by Django 5.1 on 2024-09-07 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='content',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='news',
            name='content',
            field=models.TextField(default='1'),
            preserve_default=False,
        ),
    ]
