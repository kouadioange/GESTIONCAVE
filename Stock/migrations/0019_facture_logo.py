# Generated by Django 4.1.6 on 2023-03-05 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stock', '0018_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='logo',
            field=models.ImageField(blank=True, default='index_QvapanVF.jpg', null=True, upload_to='./image/'),
        ),
    ]
