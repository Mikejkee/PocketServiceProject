# Generated by Django 4.1.7 on 2023-08-19 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PocketServiceApp', '0003_company_agent_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='products_agent', to='PocketServiceApp.product', verbose_name='Услуги'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Ремонт квартиры'), (1, 'Ремонт сантехники'), (2, 'Ремонт мебели'), (3, 'Уборка'), (4, 'Услуги красоты')], null=True, verbose_name='Тип услуги'),
        ),
    ]
