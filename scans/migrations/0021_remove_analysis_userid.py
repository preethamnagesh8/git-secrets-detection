# Generated by Django 4.1.4 on 2023-01-06 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scans', '0020_alter_analysis_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysis',
            name='userid',
        ),
    ]
