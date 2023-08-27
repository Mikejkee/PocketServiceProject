from django.db import models

SMETA_TYPES_CHOICE = [
    (0, 'Смета на работы'),
    (1, 'Смета на материалы'),
]

# TODO: Лучше проанализировать область и выписать все возможные моменты
FLAT_REPAIR = 0
PLUBMING_REPAIR = 1
FURNITURE_REPAIR = 2
CLEANING = 3
BEAUTI = 4
PRODUCT_TYPES_CHOICE = [
    (FLAT_REPAIR, 'Ремонт квартиры'),
    (PLUBMING_REPAIR, 'Ремонт сантехники'),
    (FURNITURE_REPAIR, 'Ремонт мебели'),
    (CLEANING, 'Уборка'),
    (BEAUTI, 'Услуги красоты'),
]

STATUS_TYPES_CHOICE = [
    (0, 'Не в работе'),
    (1, 'В работе'),
    (2, 'Приостановлена'),
    (3, 'Выполнена'),
]

class Registrator(models.Model):
    creation_datetime = models.DateTimeField("Время создания", auto_now_add=True)
    update_datetime = models.DateTimeField("Время обновления", auto_now_add=True)
    flag = models.BooleanField("Флаг активности", default=1)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['creation_datetime'], name='index_%(class)s_time'),
        ]


class Role(Registrator):
    # Роль каждого пользователя
    role_type = models.CharField("Роль", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.role_type

    class Meta:
        db_table = 'role'
        indexes = [] + Registrator.Meta.indexes


class Area(Registrator):
    area_name = models.CharField('Название района', max_length=255, null=True, blank=True)
    city = models.CharField('Город', max_length=255, null=True, blank=True)
    region = models.CharField('Область', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.area_name

    class Meta:
        db_table = 'area'
        indexes = [
                      models.Index(fields=['area_name'],
                                   name='index_area_name'),
                  ] + Registrator.Meta.indexes


class Person(Registrator):
    # Класс человека, от которого будут наследоваться любые типы учетных записей в боте
    name = models.CharField("Имя",
                            max_length=20,
                            null=True,
                            blank=True
                            )
    surname = models.CharField("Фамилия", max_length=20, null=True, blank=True)
    patronymic = models.CharField("Отчество", max_length=20, null=True, blank=True)
    date_of_birth = models.DateField("Дата рождения", null=True, blank=True)
    person_fio = models.CharField("ФИО",  max_length=200, null=True, blank=True)
    phone_number = models.CharField("Номер телефона", max_length=12, null=True, blank=True)
    telegram_chat_id = models.CharField('ID Чата', max_length=255, null=True, blank=True)
    username = models.CharField("Имя пользователя", max_length=20, null=True, blank=True)
    telegram_id = models.CharField("ID Телеграмм", max_length=20, null=True, blank=True)
    telegram_username = models.CharField("Пользователь Телеграмм", max_length=20, null=True, blank=True)
    telegram_name = models.CharField("Имя пользователя Телеграмм", max_length=20, null=True, blank=True)
    telegram_surname = models.CharField("Фамилия пользователя Телеграмм", max_length=20, null=True, blank=True)
    email = models.EmailField("Электронная почта", null=True, blank=True)
    background_image = models.ImageField('Аватар пользователя ',
                                         upload_to='./postgres_data/objects/persons/background/', null=True,
                                         blank=True)

    role = models.ManyToManyField(Role, blank=True, related_name='roles', verbose_name="Роли")

    class Meta:
        db_table = 'person'
        indexes = [
                      models.Index(fields=['phone_number'],
                                   name='index_persons_phone_number'),
                      models.Index(fields=['telegram_id'],
                                   name='index_persons_telegram_id'),
                      models.Index(fields=['email'],
                                   name='index_persons_email'),
                  ] + Registrator.Meta.indexes


class Company(Registrator):
    name = models.CharField(verbose_name="Название", max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    legal_address = models.CharField(verbose_name="Юридический адрес", max_length=255, null=True, blank=True)
    mail_address = models.CharField(verbose_name="Почтовый адрес", max_length=255, null=True, blank=True)
    inn = models.CharField(verbose_name="ИНН", max_length=255, null=True, blank=True)
    kpp = models.CharField(verbose_name="КПП", max_length=255, null=True, blank=True)
    ogrnip = models.CharField(verbose_name="ОГРНИП", max_length=255, null=True, blank=True)
    payment_account = models.CharField(verbose_name="Рассчетный счет", max_length=255, null=True, blank=True)
    bank = models.CharField(verbose_name="Банк", max_length=255, null=True, blank=True)
    bik = models.CharField(verbose_name="БИК", max_length=255, null=True, blank=True)
    okpo = models.CharField(verbose_name="ОКПО", max_length=255, null=True, blank=True)
    contact_phone = models.CharField(verbose_name="Контактный номер", max_length=255, null=True, blank=True)
    email = models.EmailField(verbose_name="Электронная почта", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company'


class Administrator(Person):
    whom_created = models.CharField("Создатель", max_length=20, null=True, blank=True)
    addition_information = models.TextField("Дополнительная информация", null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'administrator'


class Product(Registrator):
    # Услуги товары
    product_type = models.PositiveSmallIntegerField('Тип услуги', choices=PRODUCT_TYPES_CHOICE, blank=True, null=True)
    addition_information = models.TextField("Дополнительная информация", null=True, blank=True)
    product_image = models.ImageField('Картинка услуг', upload_to='./postgres_data/objects/products/images/', null=True,
                                      blank=True)

    def __str__(self):
        return self.addition_information

    class Meta:
        db_table = 'product'
        indexes = [
                      models.Index(fields=['product_type'],
                                   name='index_name_product'),
                  ] + Registrator.Meta.indexes

class Agent(Person):
    agent_description = models.TextField(verbose_name="Описание агента", null=True, blank=True)
    education_description = models.TextField(verbose_name="Образование", null=True, blank=True)
    work_experience = models.TextField(verbose_name="Опыт работы", null=True, blank=True)
    command_work = models.BooleanField(verbose_name="Работа в команде", null=True, blank=True)
    passport_check = models.BooleanField(verbose_name="Проверка паспорта", null=True, blank=True)
    contract_work = models.BooleanField(verbose_name="Работа по договору", null=True, blank=True)
    guarantee_period = models.TextField(verbose_name="Гарантийный период", null=True, blank=True)
    services_prices = models.TextField(verbose_name="Услуги и цены", null=True, blank=True)

    area = models.ManyToManyField(Area, blank=True, related_name='area_agents', verbose_name="Районы")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='agent_company',
                                null=True, blank=True, verbose_name="Компания")
    products = models.ManyToManyField(Product, blank=True, related_name='products_agent', verbose_name="Услуги")

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'agent'


class Client(Person):
    address = models.CharField("Адрес проживания", max_length=255, null=True, blank=True)
    addition_information = models.TextField("Дополнительная информация", null=True, blank=True)

    def __str__(self):
        return self.telegram_id

    class Meta:
        db_table = 'client'

class Order(Registrator):
    # Заявка
    name = models.CharField("Имя", max_length=255, null=True, blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, blank=True, null=True)
    deadline = models.DateTimeField("Запланированный срок конца работы", blank=True, null=True)
    addition_information = models.TextField("Дополнительная информация", null=True, blank=True)
    reminder_status = models.BooleanField("Статус напоминания", default=0)
    control_flag = models.BooleanField("Флаг новизны", default=0)
    status_flag = models.PositiveSmallIntegerField('Статус выполнения', choices=STATUS_TYPES_CHOICE,
                                                   blank=True, null=True, default=0)
    start_time = models.DateTimeField("Срок начала работы", blank=True, null=True)
    end_time = models.DateTimeField("Срок конца работы", blank=True, null=True)

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
        db_table = 'order'
        indexes = [
                      models.Index(fields=['name'],
                                   name='index_name_order'),
                  ] + Registrator.Meta.indexes


class Contract(Registrator):
    name = models.CharField("Название контракта", max_length=20, null=True, blank=True)
    contract_number = models.CharField("Номер договора", max_length=20, null=True, blank=True)
    start_date = models.DateTimeField("Дата начала работ", null=True, blank=True)
    end_date = models.DateTimeField("Дата конца работ", null=True, blank=True)

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='contact_order', null=True, blank=True,
                              verbose_name="Заявка")

    class Meta:
        db_table = 'сontract'
        indexes = [
                      models.Index(fields=['contract_number'],
                                   name='index_number_contract'),
                  ] + Registrator.Meta.indexes


class Smeta(Registrator):
    name = models.CharField("Название сметы", max_length=20, null=True, blank=True)
    smeta_type = models.PositiveSmallIntegerField("Тип сметы", choices=SMETA_TYPES_CHOICE, blank=True, null=True)
    description = models.TextField("Описание сметы", null=True, blank=True)
    name_work = models.CharField("Наименование работ/материалов", max_length=20, null=True, blank=True)
    quantity = models.CharField("Количество", max_length=20, null=True, blank=True)
    unit = models.CharField("Единица измерения", max_length=10, null=True, blank=True)
    cost = models.IntegerField("Цена", null=True, blank=True)
    price = models.IntegerField("Стоимость", null=True, blank=True)

    contract = models.ForeignKey(Contract,
                                 on_delete=models.SET_NULL,
                                 related_name='smeta_contract',
                                 null=True,
                                 blank=True,
                                 verbose_name="Смета контракта")

    class Meta:
        db_table = 'smeta'
        indexes = [

                  ] + Registrator.Meta.indexes

class OnlineTransaction(Registrator):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name='order',
                              verbose_name="Заказ")
    currency = models.CharField('Валюта', max_length=255, blank=True, null=True)
    total_amount = models.CharField('Итоговая сумма', max_length=255, blank=True, null=True)
    invoice_payload = models.CharField('Invoice payload', max_length=255, blank=True, null=True)
    provider_payment_charge_id = models.CharField('Provider Payment Charge ID', max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name="Status")
    status_str = models.CharField('Status Str', max_length=255, blank=True, null=True)
    operation = models.CharField('Operation', max_length=255, blank=True, null=True)

    masked_pan = models.CharField('Masked Pan', max_length=255, blank=True, null=True)
    bank_name = models.CharField('Bank Name', max_length=255, blank=True, null=True)
    payment_way = models.CharField('Payment Way', max_length=255, blank=True, null=True)
    expiry = models.CharField('Expiry', max_length=255, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name="Payment Time")

    class Meta:
        ordering = ['-id']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        db_table = 'Transactions'
        indexes = [] + Registrator.Meta.indexes

    def str(self):
        return f'{self.provider_payment_charge_id}'


class ImageObject(Registrator):
    person = models.ForeignKey(Person,
                               on_delete=models.SET_NULL,
                               related_name='person_image',
                               null=True,
                               blank=True,
                               verbose_name="Картинки пользователя")

    smeta = models.ForeignKey(Smeta,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              related_name='smeta_image',
                              verbose_name="Картинки для сметы"
                              )
    contract = models.ForeignKey(Contract,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='contract_image',
                                 verbose_name="Картинки для контракта"
                                 )

    image_object = models.ImageField(
        'Объект картинки',
        upload_to='./postgres_data/objects/persons/images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.image_object

    class Meta:
        db_table = 'image_object'
        indexes = [] + Registrator.Meta.indexes


class FileObject(Registrator):
    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name='person_files',
        null=True,
        blank=True,
        verbose_name="Файлы пользователя",
    )

    smeta = models.ForeignKey(Smeta,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              related_name='smeta_file',
                              verbose_name="Файлы для сметы"
                              )
    contract = models.ForeignKey(Contract,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name='contract_file',
                                 verbose_name="Файлы для контракта"
                                 )

    object_type = models.CharField("Тип объекта",
                                   max_length=100)
    file_object = models.FileField(
        'Объект файла',
        upload_to='./postgres_data/objects/persons/files/',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.file_object

    class Meta:
        db_table = 'file_object'
        indexes = [] + Registrator.Meta.indexes

