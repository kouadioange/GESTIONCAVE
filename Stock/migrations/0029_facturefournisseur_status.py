# Generated by Django 4.1.6 on 2023-03-12 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0028_alter_charges_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturefournisseur',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
