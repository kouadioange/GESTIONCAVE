# Generated by Django 4.1.6 on 2023-03-05 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0019_facture_logo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.RemoveField(
            model_name='facture',
            name='logo',
        ),
    ]
