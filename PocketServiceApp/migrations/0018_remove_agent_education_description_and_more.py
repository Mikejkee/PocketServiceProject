# Generated by Django 4.1.7 on 2023-11-07 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PocketServiceApp', '0017_alter_commentimages_table_alter_personfiles_table_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='education_description',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='services_prices',
        ),
    ]
