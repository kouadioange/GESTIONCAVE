# Generated by Django 4.1.6 on 2023-02-11 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0013_alter_typeemballage_quantite_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeemballage',
            name='quantite_stock',
            field=models.FloatField(blank=True, default=0, max_length=200, null=True),
        ),
    ]