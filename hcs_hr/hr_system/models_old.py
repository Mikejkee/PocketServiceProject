from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


class Registrator(models.Model):
    class Meta:
        abstract = True

    creation_datetime = models.DateTimeField(db_column='Creation datetime', verbose_name="Время создания",
                                             auto_now_add=True)
    update_datetime = models.DateTimeField(db_column='Update datetime', verbose_name="Время обновления",
                                           auto_now_add=True)
    flag = models.BooleanField(db_column='Flag', verbose_name="Флаг активности", default=1)


class Role(Registrator):
    # Роль каждого пользователя
    role_id = models.AutoField(primary_key=True)
    role_type = models.TextField(db_column='Role Type', verbose_name="Роль")


class TypedObject(Registrator):
    # Объект - фото, видео, аудио и т.д.
    # TODO: Можно сделать опеределнные типы объектов и залочить их (choice)
    object_type = models.TextField(db_column='Object Type', verbose_name="Тип объекта")
    object_url = models.TextField(db_column='Object Url', verbose_name="Ссылка на объект")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Person(Registrator):
    # Класс человека, от которого будут наследоваться любые типы учетных записей в боте
    class Meta:
        abstract = True

    name = models.CharField(db_column='Name', max_length=20, verbose_name="Имя")
    surname = models.CharField(db_column='Surname', max_length=20, verbose_name="Фамилия")
    patronymic = models.CharField(db_column='Patronymic', max_length=20, verbose_name="Отчество")
    date_of_birth = models.DateField(db_column='Date of birth', verbose_name="Дата рождения")
    phone_number = models.CharField(db_column='Phone number', max_length=10, verbose_name="Номер телефона")
    username = models.CharField(db_column='Username', max_length=20, verbose_name="Имя пользователя")
    telegram_id = models.CharField(db_column='Telegram id', max_length=20, verbose_name="ID Телеграмм")
    telegram_username = models.CharField(db_column='Telegram Username', max_length=20, verbose_name="Имя пользователя Телеграмм")
    email = models.EmailField(db_column='Email', verbose_name="Электронная почта")

    role = models.ManyToManyField(Role)
    background_image = GenericRelation(TypedObject)


class Agent(Person):
    # TODO: Жестко забиндить районы
    agent_description = models.TextField(db_column='Agent Description', verbose_name="Описание агента")
    education_description = models.TextField(db_column='Education Description', verbose_name="Образование")
    education_photos = GenericRelation(TypedObject)
    work_experience = models.TextField(db_column='Work Experience', verbose_name="Опыт работы")
    experience_photo = GenericRelation(TypedObject)

    areas_work = models.TextField(db_column='Areas Work', verbose_name="Районы работы")
    command_work = models.BooleanField(db_column='Command Work', verbose_name="Работа в команде")
    passport_check = models.BooleanField(db_column='Passport Check ', verbose_name="Проверка паспорта")
    contract_work = models.BooleanField(db_column='Contract Work', verbose_name="Работа по договору")
    guarantee_period = models.TextField(db_column='Guarantee Period', verbose_name="Гарантийный период")
    services_prices = models.TextField(db_column='Services Prices', verbose_name="Услуши и цены")

    # TODO: ?сущность отзывы
    comment = models.TextField(db_column='Comment', verbose_name="Образование")
    comment_photos = GenericRelation(TypedObject)


class Client(Person):
    address = models.TextField(db_column='Address', verbose_name="Адрес проживания")
    addition_information = models.TextField(db_column='Addition information', verbose_name="Дополнительная информация")
    object_information = models.TextField(db_column='Object Information', verbose_name="Информация об объекте проживания")


class Administrator(Person):
    whom_created = models.CharField(db_column='Whom Created', max_length=20, verbose_name="Кто создатель")
    addition_information = models.TextField(db_column='Addition information', verbose_name="Дополнительная информация")


class Order(Registrator):
    # TODO: Непосредственно сама транзакция между Agent и Client (договор об услугах)
    #       Здесь пока не думал
    price = models.TextField(db_column='Price', verbose_name="Цена")







