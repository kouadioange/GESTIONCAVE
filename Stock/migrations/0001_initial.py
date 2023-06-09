# Generated by Django 4.1.6 on 2023-02-10 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(blank=True, max_length=200, null=True)),
                ('reference', models.CharField(blank=True, max_length=200, null=True)),
                ('categorie', models.CharField(blank=True, choices=[('VIN', 'VIN'), ('SUCRERIE', 'SUCRERIE'), ('BIERE', 'BIERE'), ('LIQUEUR', 'LIQUEUR'), ('EAU', 'EAU'), ('CHAMPAGNE', 'CHAMPAGNE'), ('ENERGIE', 'ENERGIE')], max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='./image/')),
            ],
        ),
    ]
