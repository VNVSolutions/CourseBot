# Generated by Django 3.1.1 on 2024-04-10 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0014_auto_20240410_1320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interview',
            name='img',
        ),
        migrations.RemoveField(
            model_name='labormarket',
            name='img',
        ),
    ]
