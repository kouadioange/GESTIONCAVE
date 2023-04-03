# Generated by Django 4.1.6 on 2023-03-21 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0031_approvision_reference'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_prenom', models.CharField(blank=True, max_length=300, null=True)),
                ('adresse', models.CharField(blank=True, max_length=200, null=True)),
                ('ville', models.CharField(blank=True, max_length=200, null=True)),
                ('contact', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
