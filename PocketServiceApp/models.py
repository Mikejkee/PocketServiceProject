from django.db import models

SMETA_TYPES_CHOICE = [
    (0, 'Смета на работы'),
    (1, 'Смета на материалы'),
]

# TODO: Лучше проанализировать область и выписать все возможные моменты
FLAT_REPAIR = 0
PLUBMING_REPAIR = 1
FURNITURE_REPAIR = 2
BEAUTI = 3
CLEANING = 4
PRODUCT_TYPES_CHOICE = [
    (FLAT_REPAIR, 'Ремонт квартиры'),
    (PLUBMING_REPAIR, 'Ремонт техники'),
    (FURNITURE_REPAIR, 'Ремонт мебели'),
    (BEAUTI, 'Услуги красоты'),
    (CLEANING, 'Уборка'),
]

STATUS_TYPES_CHOICE = [
    (0, 'Не в работе'),
    (1, 'В работе'),
    (2, 'Приостановлена'),
    (3, 'Выполнена'),
]

RATING_CHOICES = (
    (1, '1 звезда'),
    (2, '2 звезды'),
    (3, '3 звезды'),
    (4, '4 звезды'),
    (5, '5 звезд')
)


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
    person_fio = models.CharField("ФИО", max_length=200, null=True, blank=True)
    phone_number = models.CharField("Номер телефона", max_length=12, null=True, blank=True)
    telegram_chat_id = models.CharField('ID Чата', max_length=255, null=True, blank=True)
    telegram_id = models.CharField("ID Телеграмм", max_length=20, null=True, blank=True)
    telegram_username = models.CharField("Username аккаунта Телеграмм", max_length=20, null=True, blank=True)
    telegram_name = models.CharField("Имя пользователя Телеграмм", max_length=20, null=True, blank=True)
    telegram_surname = models.CharField("Фамилия пользователя Телеграмм", max_length=20, null=True, blank=True)
    email = models.EmailField("Электронная почта", null=True, blank=True)
    background_image = models.ImageField('Аватар пользователя ',
                                         upload_to='./postgres_data/objects/persons/background/', null=True,
                                         blank=True)

    role = models.ManyToManyField(Role, blank=True, related_name='roles', verbose_name="Роли")

    def __str__(self):
        if self.telegram_username:
            return self.telegram_username
        else:
            return self.telegram_id

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
    name = models.CharField("Название", max_length=255, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    legal_address = models.CharField("Юридический адрес", max_length=255, null=True, blank=True)
    mail_address = models.CharField("Почтовый адрес", max_length=255, null=True, blank=True)
    inn = models.CharField("ИНН", max_length=255, null=True, blank=True)
    kpp = models.CharField("КПП", max_length=255, null=True, blank=True)
    ogrnip = models.CharField("ОГРНИП", max_length=255, null=True, blank=True)
    payment_account = models.CharField("Рассчетный счет", max_length=255, null=True, blank=True)
    bank = models.CharField("Банк", max_length=255, null=True, blank=True)
    bik = models.CharField("БИК", max_length=255, null=True, blank=True)
    okpo = models.CharField("ОКПО", max_length=255, null=True, blank=True)
    contact_phone = models.CharField("Контактный номер", max_length=255, null=True, blank=True)
    email = models.EmailField("Электронная почта", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'company'


class Administrator(Person):
    whom_created = models.CharField("Создатель", max_length=20, null=True, blank=True)
    addition_information = models.TextField("Дополнительная информация", null=True, blank=True)

    def __str__(self):
        if self.telegram_username:
            return self.telegram_username
        else:
            return self.telegram_id

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
    agent_description = models.TextField("Описание агента", null=True, blank=True)
    # education_description = models.TextField("Образование", null=True, blank=True)
    work_experience = models.TextField("Опыт работы", null=True, blank=True)
    command_work = models.BooleanField("Работа в команде", null=True, blank=True)
    passport_check = models.BooleanField("Проверка паспорта", null=True, blank=True)
    contract_work = models.BooleanField("Работа по договору", null=True, blank=True)
    guarantee_period = models.TextField("Гарантийный период", null=True, blank=True)
    # services_prices = models.TextField("Услуги и цены", null=True, blank=True)

    area = models.ManyToManyField(Area, blank=True, related_name='area_agents', verbose_name="Районы")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='agent_company',
                                null=True, blank=True, verbose_name="Компания")
    products = models.ManyToManyField(Product, blank=True, related_name='products_agent', verbose_name="Услуги")

    def __str__(self):
        username, fio = ("", "")
        if self.telegram_username:
            username = "(@{})".format(self.telegram_username)
        if self.person_fio:
            fio = self.person_fio
        return "{}{}".format(fio, username)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        clients = Client.objects.filter(telegram_id=str(self.telegram_id))

        if clients.count() > 0:
            clients.last().delete()

    class Meta:
        db_table = 'agent'


class Price(Registrator):
    price_value = models.CharField("Цена", max_length=30, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_price',
                                null=True, blank=True, verbose_name="Услуга")
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, related_name='agent_product_price',
                              null=True, blank=True, verbose_name="Агент")

    def save(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        if not self.pk:
            agent_products = self.agent.products
            if self.product in agent_products.all():
                super(Price, self).save(*args, **kwargs)
            else:
                raise ValueError("У агента нет такой услуги")
        else:
            super(Price, self).save(*args, **kwargs)

    class Meta:
        db_table = 'price'


class Specialization(Registrator):
    name = models.CharField("Название специализации", max_length=50, null=True, blank=True)
    specialization_description = models.TextField("Описание специализации", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'specialization'


class University(Registrator):
    name = models.CharField("Название института/колледжа/школы", max_length=70, null=True, blank=True)
    town = models.CharField("Город", max_length=70, null=True, blank=True)
    country = models.CharField("Страна", max_length=70, null=True, blank=True)
    university_description = models.TextField("Описание места учебы", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'university'


class Education(Registrator):
    period_start = models.DateField("Срок начала учебы", blank=True, null=True)
    period_end = models.DateField("Срок конца учебы", blank=True, null=True)
    document_check = models.BooleanField("Проверка документа", null=True, blank=True)

    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, related_name='education',
                              null=True, blank=True, verbose_name="Агент")
    university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='education', verbose_name="Место учебы")
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, blank=True, null=True,
                                       related_name='education', verbose_name="Специальность")

    def __str__(self):
        if self.agent.telegram_username:
            return '{}_{}_{}'.format(self.agent.telegram_username, self.university.name, self.specialization.name)
        else:
            return '{}_{}_{}'.format(self.agent.telegram_id, self.university.name, self.specialization.name)

    class Meta:
        db_table = 'education'


class Client(Person):
    address = models.CharField("Адрес проживания", max_length=255, null=True, blank=True)
    addition_information = models.TextField("Дополнительная информация", null=True, blank=True)

    def __str__(self):
        if self.telegram_username:
            return self.telegram_username
        else:
            return self.telegram_id

    class Meta:
        db_table = 'client'


class Order(Registrator):
    # Заявка
    name = models.CharField("Имя", max_length=255, null=True, blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, blank=True, null=True)
    deadline = models.DateField("Запланированный срок конца работы", blank=True, null=True)
    addition_information = models.TextField("Дополнительная информация", null=True, blank=True)
    reminder_status = models.BooleanField("Статус напоминания", default=0)
    control_flag = models.BooleanField("Флаг новизны", default=0)
    status_flag = models.PositiveSmallIntegerField('Статус выполнения', choices=STATUS_TYPES_CHOICE,
                                                   blank=True, null=True, default=0)
    start_time = models.DateField("Срок начала работы", blank=True, null=True)
    end_time = models.DateField("Срок конца работы", blank=True, null=True)

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name='client_orders', null=True, blank=True,
                               verbose_name="Клиент")
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, related_name='agent_orders', null=True, blank=True,
                              verbose_name="Агент")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_orders', null=True,
                                blank=True, verbose_name="Продукт")
    administrator = models.ForeignKey(Administrator, on_delete=models.SET_NULL, related_name='product_orders',
                                      null=True, blank=True, verbose_name="Администратор")

    def __str__(self):
        product = "{}".format(self.product.__str__())
        time = "Создана: {}".format(self.creation_datetime)
        return '«{}» {}[{}]'.format(product, time, self.id)

    class Meta:
        db_table = 'order'
        indexes = [
                      models.Index(fields=['name'],
                                   name='index_name_order'),
                  ] + Registrator.Meta.indexes


class Contract(Registrator):
    name = models.CharField("Название контракта", max_length=20, null=True, blank=True)
    contract_number = models.CharField("Номер договора", max_length=20, null=True, blank=True)
    start_date = models.DateField("Дата начала работ", null=True, blank=True)
    end_date = models.DateField("Дата конца работ", null=True, blank=True)

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
    status = models.BooleanField("Status", default=False)
    status_str = models.CharField('Status Str', max_length=255, blank=True, null=True)
    operation = models.CharField('Operation', max_length=255, blank=True, null=True)

    masked_pan = models.CharField('Masked Pan', max_length=255, blank=True, null=True)
    bank_name = models.CharField('Bank Name', max_length=255, blank=True, null=True)
    payment_way = models.CharField('Payment Way', max_length=255, blank=True, null=True)
    expiry = models.CharField('Expiry', max_length=255, blank=True, null=True)
    payment_date = models.DateTimeField("Payment Time", blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        db_table = 'Transactions'
        indexes = [] + Registrator.Meta.indexes

    def str(self):
        return f'{self.provider_payment_charge_id}'


class Comment(Registrator):
    rating = models.PositiveSmallIntegerField('Рейтинг', choices=RATING_CHOICES, blank=True, null=True)
    text = models.TextField("Текст комментария", null=True, blank=True)

    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, related_name='comments', null=True, blank=True,
                              verbose_name="Агент")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name='comments', null=True, blank=True,
                               verbose_name="Клиент")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='comments', null=True, blank=True,
                              verbose_name="Заявка")

    def __str__(self):
        return 'Comment by {} on {} for {}'.format(self.agent_id, self.client_id, self.order_id)

    class Meta:
        db_table = 'comment'


class CommentImages(Registrator):
    image_object = models.ImageField('Картинка', upload_to='./postgres_data/objects/comments/images/',
                                     null=True, blank=True)

    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, related_name='images', null=True, blank=True,
                                verbose_name="Фото к отзыву")

    def __str__(self):
        return self.image_object.url

    class Meta:
        db_table = 'comment_image'
        indexes = [] + Registrator.Meta.indexes


class PersonImages(Registrator):
    image_object = models.ImageField('Картинка', upload_to='./postgres_data/objects/persons/images/',
                                     null=True, blank=True)

    person = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='images', null=True, blank=True,
                               verbose_name="Картинки пользователя")

    def __str__(self):
        return self.image_object

    class Meta:
        db_table = 'person_image'
        indexes = [] + Registrator.Meta.indexes


class PersonFiles(Registrator):
    object_type = models.CharField("Тип файла", max_length=100)
    file_object = models.FileField('Файл', upload_to='./postgres_data/objects/persons/files/', null=True, blank=True)

    person = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='files', null=True, blank=True,
                               verbose_name="Файлы пользователя")

    def __str__(self):
        return self.file_object

    class Meta:
        db_table = 'person_file'
        indexes = [] + Registrator.Meta.indexes
