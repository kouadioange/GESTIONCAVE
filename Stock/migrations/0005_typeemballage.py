# Generated by Django 4.1.6 on 2023-02-10 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0004_rename_date_produit_date_creation'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeEmballage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, choices=[('DETAIL', 'DETAIL'), ('GROS', 'GROS')], max_length=200, null=True)),
                ('prix_achat', models.FloatField(blank=True, max_length=200, null=True)),
                ('prix_vente', models.FloatField(blank=True, max_length=200, null=True)),
                ('nombre_unite', models.FloatField(blank=True, max_length=200, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('produit', models.ForeignKey(blank=True, max_length=200, null=True, on_delete=django.db.models.deletion.CASCADE, to='Stock.produit')),
            ],
        ),
    ]