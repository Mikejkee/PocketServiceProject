# Generated by Django 4.1.7 on 2023-09-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PocketServiceApp', '0007_order_end_time_order_start_time_alter_order_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='username',
        ),
        migrations.AlterField(
            model_name='person',
            name='telegram_username',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Username аккаунта Телеграмм'),
        ),
    ]
