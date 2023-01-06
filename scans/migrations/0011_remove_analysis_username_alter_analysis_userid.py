# Generated by Django 4.1.4 on 2023-01-06 06:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scans', '0010_alter_analysis_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysis',
            name='username',
        ),
        migrations.AlterField(
            model_name='analysis',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
