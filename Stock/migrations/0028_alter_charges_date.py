# Generated by Django 4.1.6 on 2023-03-10 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0027_charges_depenses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charges',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
