# Generated by Django 4.1.6 on 2023-04-03 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0041_rename_faccture_facture'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Remise',
        ),
    ]
