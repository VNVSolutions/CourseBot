# Generated by Django 3.1.1 on 2024-04-08 11:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0012_resume_tongue'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resume',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='user',
            field=models.CharField(max_length=100, verbose_name='Користувач'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='resume_file',
            field=models.FileField(blank=True, upload_to='resumes/'),
        ),
    ]
