# Generated by Django 4.1.6 on 2023-03-13 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0029_facturefournisseur_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approvision',
            name='facture_fournisseur',
        ),
    ]
