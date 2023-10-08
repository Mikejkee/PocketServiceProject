# Generated by Django 4.1.7 on 2023-10-06 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PocketServiceApp', '0015_alter_education_agent_alter_education_specialization_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('rating', models.PositiveSmallIntegerField(blank=True, choices=[(1, '1 звезда'), (2, '2 звезды'), (3, '3 звезды'), (4, '4 звезды'), (5, '5 звезд')], null=True, verbose_name='Рейтинг')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст комментария')),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='PocketServiceApp.agent', verbose_name='Агент')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='PocketServiceApp.client', verbose_name='Клиент')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='PocketServiceApp.order', verbose_name='Заявка')),
            ],
            options={
                'db_table': 'comment',
            },
        ),
        migrations.CreateModel(
            name='CommentImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('image_object', models.ImageField(blank=True, null=True, upload_to='./postgres_data/objects/comments/images/', verbose_name='Картинка')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='PocketServiceApp.comment', verbose_name='Фото к отзыву')),
            ],
            options={
                'db_table': 'comment_images',
            },
        ),
        migrations.CreateModel(
            name='PersonFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('object_type', models.CharField(max_length=100, verbose_name='Тип файла')),
                ('file_object', models.FileField(blank=True, null=True, upload_to='./postgres_data/objects/persons/files/', verbose_name='Файл')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='PocketServiceApp.person', verbose_name='Файлы пользователя')),
            ],
            options={
                'db_table': 'person_files',
            },
        ),
        migrations.CreateModel(
            name='PersonImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Время обновления')),
                ('flag', models.BooleanField(default=1, verbose_name='Флаг активности')),
                ('image_object', models.ImageField(blank=True, null=True, upload_to='./postgres_data/objects/persons/images/', verbose_name='Картинка')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='PocketServiceApp.person', verbose_name='Картинки пользователя')),
            ],
            options={
                'db_table': 'person_images',
            },
        ),
        migrations.RemoveField(
            model_name='imageobject',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='imageobject',
            name='person',
        ),
        migrations.RemoveField(
            model_name='imageobject',
            name='smeta',
        ),
        migrations.DeleteModel(
            name='FileObject',
        ),
        migrations.DeleteModel(
            name='ImageObject',
        ),
        migrations.AddIndex(
            model_name='personimages',
            index=models.Index(fields=['creation_datetime'], name='index_personimages_time'),
        ),
        migrations.AddIndex(
            model_name='personfiles',
            index=models.Index(fields=['creation_datetime'], name='index_personfiles_time'),
        ),
        migrations.AddIndex(
            model_name='commentimages',
            index=models.Index(fields=['creation_datetime'], name='index_commentimages_time'),
        ),
    ]