# Generated by Django 4.1.7 on 2023-05-29 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr_system', '0013_remove_fileobject_contract_remove_fileobject_person_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Название контракта')),
                ('contract_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер договора')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата начала работ')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата конца работ')),
            ],
            options={
                'db_table': 'сontract',
            },
        ),
        migrations.CreateModel(
            name='FileObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('object_type', models.CharField(max_length=100, verbose_name='Тип объекта')),
                ('file_object', models.FileField(blank=True, null=True, upload_to='./postgres_data/objects/persons/files/', verbose_name='Объект файла')),
            ],
            options={
                'db_table': 'file_object',
            },
        ),
        migrations.CreateModel(
            name='ImageObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('image_object', models.ImageField(blank=True, null=True, upload_to='./postgres_data/objects/persons/images/', verbose_name='Объект картинки')),
            ],
            options={
                'db_table': 'image_object',
            },
        ),
        migrations.CreateModel(
            name='OnlineTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('currency', models.CharField(blank=True, max_length=255, null=True, verbose_name='Валюта')),
                ('total_amount', models.CharField(blank=True, max_length=255, null=True, verbose_name='Итоговая сумма')),
                ('invoice_payload', models.CharField(blank=True, max_length=255, null=True, verbose_name='Invoice payload')),
                ('provider_payment_charge_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Provider Payment Charge ID')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('status_str', models.CharField(blank=True, max_length=255, null=True, verbose_name='Status Str')),
                ('operation', models.CharField(blank=True, max_length=255, null=True, verbose_name='Operation')),
                ('masked_pan', models.CharField(blank=True, max_length=255, null=True, verbose_name='Masked Pan')),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Bank Name')),
                ('payment_way', models.CharField(blank=True, max_length=255, null=True, verbose_name='Payment Way')),
                ('expiry', models.CharField(blank=True, max_length=255, null=True, verbose_name='Expiry')),
                ('payment_date', models.DateTimeField(blank=True, null=True, verbose_name='Payment Time')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'db_table': 'Transactions',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена')),
                ('deadline', models.DateTimeField(blank=True, null=True, verbose_name='Срок конца работы')),
                ('addition_information', models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')),
                ('reminder_status', models.BooleanField(default=0, verbose_name='Статус напоминания')),
                ('control_flag', models.BooleanField(default=0, verbose_name='Флаг новизны')),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('product_type', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Ремонт сантехники'), (1, 'Ремонт мебели'), (2, 'Уборка')], null=True, verbose_name='Тип услуги')),
                ('addition_information', models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='./postgres_data/objects/products/images/', verbose_name='Картинка услуг')),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Smeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Название сметы')),
                ('smeta_type', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Смета на работы'), (1, 'Смета на материалы')], null=True, verbose_name='Тип сметы')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание сметы')),
                ('name_work', models.CharField(blank=True, max_length=20, null=True, verbose_name='Наименование работ/материалов')),
                ('quantity', models.CharField(blank=True, max_length=20, null=True, verbose_name='Количество')),
                ('unit', models.CharField(blank=True, max_length=10, null=True, verbose_name='Единица измерения')),
                ('cost', models.IntegerField(blank=True, null=True, verbose_name='Цена')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Стоимость')),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='smeta_contract', to='hr_system.contract', verbose_name='Смета контракта')),
            ],
            options={
                'db_table': 'smeta',
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['product_type'], name='index_name_product'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['creation_datetime'], name='index_product_time'),
        ),
        migrations.AddField(
            model_name='order',
            name='administrator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_orders', to='hr_system.administrator', verbose_name='Администратор'),
        ),
        migrations.AddField(
            model_name='order',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_orders', to='hr_system.agent', verbose_name='Агент'),
        ),
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_orders', to='hr_system.client', verbose_name='Клиент'),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_orders', to='hr_system.product', verbose_name='Продукт'),
        ),
        migrations.AddField(
            model_name='onlinetransaction',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='hr_system.order', verbose_name='Заказ'),
        ),
        migrations.AddField(
            model_name='imageobject',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contract_image', to='hr_system.contract', verbose_name='Картинки для контракта'),
        ),
        migrations.AddField(
            model_name='imageobject',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_image', to='hr_system.person', verbose_name='Картинки пользователя'),
        ),
        migrations.AddField(
            model_name='imageobject',
            name='smeta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='smeta_image', to='hr_system.smeta', verbose_name='Картинки для сметы'),
        ),
        migrations.AddField(
            model_name='fileobject',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contract_file', to='hr_system.contract', verbose_name='Файлы для контракта'),
        ),
        migrations.AddField(
            model_name='fileobject',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_files', to='hr_system.person', verbose_name='Файлы пользователя'),
        ),
        migrations.AddField(
            model_name='fileobject',
            name='smeta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='smeta_file', to='hr_system.smeta', verbose_name='Файлы для сметы'),
        ),
        migrations.AddField(
            model_name='contract',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_order', to='hr_system.order', verbose_name='Заявка'),
        ),
        migrations.AddIndex(
            model_name='smeta',
            index=models.Index(fields=['creation_datetime'], name='index_smeta_time'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['name'], name='index_name_order'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['creation_datetime'], name='index_order_time'),
        ),
        migrations.AddIndex(
            model_name='onlinetransaction',
            index=models.Index(fields=['creation_datetime'], name='index_onlinetransaction_time'),
        ),
        migrations.AddIndex(
            model_name='imageobject',
            index=models.Index(fields=['creation_datetime'], name='index_imageobject_time'),
        ),
        migrations.AddIndex(
            model_name='fileobject',
            index=models.Index(fields=['creation_datetime'], name='index_fileobject_time'),
        ),
        migrations.AddIndex(
            model_name='contract',
            index=models.Index(fields=['contract_number'], name='index_number_contract'),
        ),
        migrations.AddIndex(
            model_name='contract',
            index=models.Index(fields=['creation_datetime'], name='index_contract_time'),
        ),
    ]
