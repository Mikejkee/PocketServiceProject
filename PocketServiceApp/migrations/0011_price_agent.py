# Generated by Django 4.1.7 on 2023-09-20 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PocketServiceApp', '0010_price_price_index_price_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_product_price', to='PocketServiceApp.agent', verbose_name='Агент'),
        ),
    ]
