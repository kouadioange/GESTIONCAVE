# Generated by Django 4.1.6 on 2023-03-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0030_remove_approvision_facture_fournisseur'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvision',
            name='reference',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
