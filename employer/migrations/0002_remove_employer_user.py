# Generated by Django 5.1.2 on 2024-10-27 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='user',
        ),
    ]
