# Generated by Django 4.1.6 on 2023-02-11 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Stock', '0011_alter_typeemballage_libelle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvision',
            name='save_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
