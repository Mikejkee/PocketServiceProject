# Generated by Django 4.1.7 on 2023-11-07 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PocketServiceApp', '0019_university_town'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='country',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Страна'),
        ),
    ]
