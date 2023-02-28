from django.db import models


class Registrator(models.Model):
    creation_datetime = models.DateTimeField("Время создания", auto_now_add=True)
    update_datetime = models.DateTimeField("Время обновления", auto_now_add=True)
    flag = models.BooleanField("Флаг активности", default=1)

    class Meta:
        abstract = True


class Role(Registrator):
    # Роль каждого пользователя
    role_type = models.CharField("Роль", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.role_type

    class Meta:
        db_table = 'roles'
        indexes = [
            models.Index(fields=['creation_datetime'],
                         name='index_roles_creation_datetime'),
        ]


class Area(Registrator):
    area_name = models.CharField('Название района', max_length=255, null=True, blank=True)
    city = models.CharField('Город', max_length=255, null=True, blank=True)
    region = models.CharField('Область', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.area_name

    class Meta:
        db_table = 'areas'
        indexes = [
       
            models.Index(fields=['area_name'],
                         name='index_area_name'),
            models.Index(fields=['creation_datetime'],
                         name='index_roles_creation_datetime'),
        ]


class Person(Registrator):
    # Класс человека, от которого будут наследоваться любые типы учетных записей в боте
    name = models.CharField("Имя", max_length=20, null=True, blank=True)
    surname = models.CharField("Фамилия", max_length=20, null=True, blank=True)
    patronymic = models.CharField("Отчество", max_length=20, null=True, blank=True)
    date_of_birth = models.DateField("Дата рождения", null=True, blank=True)
    phone_number = models.CharField("Номер телефона", max_length=10, null=True, blank=True)
    username = models.CharField("Имя пользователя", max_length=20, null=True, blank=True)
    telegram_id = models.CharField("ID Телеграмм", max_length=20, null=True, blank=True)
    telegram_username = models.CharField("Имя пользователя Телеграмм", max_length=20, null=True, blank=True)
    email = models.EmailField("Электронная почта", null=True, blank=True)
    background_image = models.ImageField('Аватар пользователя ', upload_to='person_images/background/', null=True,
                                         blank=True)

    role = models.ManyToManyField(Role, blank=True, related_name='roles', verbose_name="Роли")

    class Meta:
        db_table = 'persons'
        indexes = [
            models.Index(fields=['phone_number'],
                         name='index_persons_phone_number'),
            models.Index(fields=['telegram_id'],
                         name='index_persons_telegram_id'),
            models.Index(fields=['email'],
                         name='index_persons_email'),
            models.Index(fields=['creation_datetime'],
                         name='index_roles_creation_datetime'),
        ]


class ImageObject(Registrator):
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='person_image', null=True, blank=True,
                               verbose_name="Пользователь")

    person_image = models.ImageField('Картинка пользователя', upload_to='person_images/', null=True, blank=True)

    def __str__(self):
        return self.person_image

    class Meta:
        db_table = 'image_objects'
   

class FileObject(Registrator):
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='person_files', null=True, blank=True,
                               verbose_name="Пользователь")

    object_type = models.CharField("Тип объекта", max_length=100)
    person_file = models.FileField('Файл пользователя', upload_to='person_files/', null=True, blank=True)

    def __str__(self):
        return self.person_file

    class Meta:
        db_table = 'file_objects'
    

class Agent(Person):
    agent_description = models.TextField(verbose_name="Описание агента", null=True, blank=True)
    education_description = models.TextField(verbose_name="Образование", null=True, blank=True)
    work_experience = models.TextField(verbose_name="Опыт работы", null=True, blank=True)
    command_work = models.BooleanField(verbose_name="Работа в команде", null=True, blank=True)
    passport_check = models.BooleanField(verbose_name="Проверка паспорта", null=True, blank=True)
    contract_work = models.BooleanField(verbose_name="Работа по договору", null=True, blank=True)
    guarantee_period = models.TextField(verbose_name="Гарантийный период", null=True, blank=True)
    services_prices = models.TextField(verbose_name="Услуги и цены", null=True, blank=True)

    area = models.ForeignKey(Area, on_delete=models.SET_NULL, related_name='area_agents', null=True, blank=True,
                             verbose_name="Район")
    #comment = models.TextField(verbose_name="Образование")

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'agents'
        indexes = [
            models.Index(fields=['phone_number'],
                         name='index_agents_phone_number'),
            models.Index(fields=['username'],
                         name='index_agents_username'),
            models.Index(fields=['telegram_id'],
                         name='index_agents_telegram_id'),
            models.Index(fields=['email'],
                         name='index_agents_email'),
            models.Index(fields=['creation_datetime'],
                         name='index_roles_creation_datetime'),
            # TODO: индексы по типу выполняемых работ (перед этим их типизировать одинаково списком)
        ]



class Client(Person):
    address = models.CharField("Адрес проживания", max_length=255, null=True, blank=True)
    addition_information = models.TextField("Дополнительная информация", null=True, blank=True)
    object_information = models.TextField("Информация об объекте проживания", null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'clients'
        indexes = [
            models.Index(fields=['phone_number'],
                         name='index_clients_phone_number'),
            models.Index(fields=['telegram_id'],
                         name='index_clients_telegram_id'),
            models.Index(fields=['email'],
                         name='index_clients_email'),
            models.Index(fields=['creation_datetime'],
                         name='index_roles_creation_datetime'),
        ]


class Administrator(Person):
    whom_created = models.CharField("Создатель", max_length=20, null=True, blank=True)
    addition_information = models.TextField("Дополнительная информация", null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'administrators'
        indexes = [
            models.Index(fields=['creation_datetime'],
                         name='index_roles_creation_datetime'),
        ]


# TODO: Лучше проанализировать область и выписать все возможные моменты
PLUBMING_REPAIR = 0
FURNITURE_REPAIR = 1
CLEANING = 2
PRODUCT_TYPES_CHOICE = [
    (PLUBMING_REPAIR, 'Ремонт сантехники'),
    (FURNITURE_REPAIR, 'Ремонт мебели'),
    (CLEANING, 'Уборка'),
]


class Product(Registrator):  # услуги товары
    name = models.CharField("Имя", max_length=255, null=True, blank=True)
    product_type = models.PositiveSmallIntegerField('Тип услуги', choices=PRODUCT_TYPES_CHOICE, blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, blank=True, null=True)
    addition_information = models.TextField("Дополнительная информация", null=True, blank=True)
    product_image = models.ImageField('Картинка услуг', upload_to='product_images/', null=True,  blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, related_name='agent_products', null=True, blank=True,
                              verbose_name="Агент")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=['name'],
                         name='index_name_product'),
            models.Index(fields=['creation_datetime'],
                         name='index_roles_creation_datetime'),
        ]


class Order(Registrator):
    name = models.CharField("Имя", max_length=255, null=True, blank=True)
    result_price = models.DecimalField("Цена", max_digits=10, decimal_places=2, blank=True, null=True)
    deadline = models.DateTimeField("Срок конца работы", blank=True, null=True)
    addition_information = models.TextField("Дополнительная информация", null=True, blank=True)

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name='client_orders', null=True, blank=True,
                               verbose_name="Клиент")
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, related_name='agent_orders', null=True, blank=True,
                              verbose_name="Агент")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_orders', null=True,
                                blank=True, verbose_name="Продукт")
    administrator = models.ForeignKey(Administrator, on_delete=models.SET_NULL, related_name='product_orders',
                                      null=True, blank=True, verbose_name="Администратор")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'orders'
        indexes = [
            models.Index(fields=['name'],
                         name='index_name_order'),
            models.Index(fields=['creation_datetime'],
                         name='index_roles_creation_datetime'),
           
        ]



class OnlinePayment(Registrator):
    # тут поля позже скину - оплата через эквайринг - или покупка товара-услуги или покупка подписки на платформе в
    # форме автоплатежей
    pass







