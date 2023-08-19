# Generated by Django 4.1.7 on 2023-08-18 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PocketServiceApp', '0002_person_person_fio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('legal_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Юридический адрес')),
                ('mail_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Почтовый адрес')),
                ('inn', models.CharField(blank=True, max_length=255, null=True, verbose_name='ИНН')),
                ('kpp', models.CharField(blank=True, max_length=255, null=True, verbose_name='КПП')),
                ('ogrnip', models.CharField(blank=True, max_length=255, null=True, verbose_name='ОГРНИП')),
                ('payment_account', models.CharField(blank=True, max_length=255, null=True, verbose_name='Рассчетный счет')),
                ('bank', models.CharField(blank=True, max_length=255, null=True, verbose_name='Банк')),
                ('bik', models.CharField(blank=True, max_length=255, null=True, verbose_name='БИК')),
                ('okpo', models.CharField(blank=True, max_length=255, null=True, verbose_name='ОКПО')),
                ('contact_phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Контактный номер')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Электронная почта')),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.AddField(
            model_name='agent',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_company', to='PocketServiceApp.company', verbose_name='Компания'),
        ),
    ]
