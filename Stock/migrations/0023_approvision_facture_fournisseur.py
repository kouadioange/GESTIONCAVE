# Generated by Django 4.1.6 on 2023-03-07 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0022_facturefournisseur'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvision',
            name='facture_fournisseur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Stock.facturefournisseur'),
        ),
    ]