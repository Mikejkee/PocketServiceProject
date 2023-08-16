from django.db import transaction, IntegrityError
from datetime import datetime

from PocketServiceApp.models import Client, Role, Product, Administrator, Smeta, Order, Agent, Person


head_admin_role = Role.objects.filter(role_type='Главный администратор').last()
head_admin = Administrator.objects.filter(role=head_admin_role).last()


def save_user(role_type, name, surname, patronymic, person_fio, date_of_birth,
              phone_number, username, telegram_chat_id,
              telegram_id, telegram_username, telegram_name,
              telegram_surname, email, background_image, address,
              addition_information, object_information):

    ### TODO: Расписать обновление специфичных полей для агента и админа (наподобие с try-except для полей клиента)
    ###       тоже самое и со созданием админов и агентов
    if "клиент" in role_type:
        persons = Client.objects.filter(telegram_id=str(telegram_id))
    elif "агент" in role_type:
        persons = Agent.objects.filter(telegram_id=str(telegram_id))
    elif "агент" in role_type:
        persons = Administrator.objects.filter(telegram_id=str(telegram_id))

    with transaction.atomic():
        if persons.count() > 0:
            person = persons.last()
            if name:
                person.name = name
            if surname:
                person.surname = surname
            if patronymic:
                person.patronymic = patronymic
            if person_fio:
                person.person_fio = person_fio
            if date_of_birth:
                person.date_of_birth = date_of_birth
            if phone_number:
                person.phone_number = phone_number
            if username:
                person.username = username
            if telegram_chat_id:
                person.telegram_chat_id = telegram_chat_id
            if telegram_username:
                person.telegram_username = telegram_username
            if email:
                person.email = email
            if background_image:
                person.background_image = background_image
            try:
                if address:
                    person.address = address
            except AttributeError:
                pass
            try:
                if addition_information:
                    person.addition_information = addition_information
            except AttributeError:
                pass
            try:
                if object_information:
                    person.object_information = object_information
            except AttributeError:
                pass
            person.save()
            print("User updated")
            return True
        else:
            role = Role.objects.filter(role_type=str(role_type)).last()
            try:
                new_user = Client.objects.create(name=name, surname=surname, patronymic=patronymic,
                                                 date_of_birth=date_of_birth, phone_number=phone_number,
                                                 username=phone_number, telegram_chat_id=telegram_chat_id,
                                                 telegram_id=telegram_id, telegram_username=telegram_username,
                                                 telegram_name=telegram_name, telegram_surname=telegram_surname,
                                                 email=email, background_image=background_image, address=address,
                                                 addition_information=addition_information,
                                                 object_information=object_information)
                new_user.save()
                new_user.role.add(role)
                print("User created")
                return True
            except Exception as e:
                print(e)
                return False


def create_order(client_id, agent_id, product_type, product_addition_information,
                 order_name, price, deadline, addition_information):
    print('hui')
    client = Client.objects.filter(telegram_id=str(client_id)).last()
    print(client)
    agent = Agent.objects.filter(telegram_id=str(agent_id)).last()
    print(agent)
    product = Product.objects.filter(product_type=product_type,
                                     addition_information=product_addition_information).last()
    print(product)
    print('order create start')
    with transaction.atomic():
        try:
            new_order = Order.objects.create(name=order_name, price=price, deadline=deadline,
                                             addition_information=addition_information,
                                             administrator=head_admin, client=client,
                                             agent=agent, product=product)
            print("Order created")
            return new_order.id
        except Exception as e:
            print(e)
            return False


def update_order(order_id, reminder_status=None, control_flag=None):
    with transaction.atomic():
        orders = Order.objects.filter(id=str(order_id))
        if orders.count() > 0:
            if reminder_status is not None:
                orders.update(reminder_status=reminder_status)
            if control_flag is not None:
                orders.update(control_flag=control_flag)
            return True
        else:
            return False


async def tg_message(bot, telegram_id, content, messages=None):
    try:
        await bot.send_message(chat_id=telegram_id, text=content, parse_mode='HTML')
        if messages:
            for msg in messages:
                await bot.delete_message(chat_id=telegram_id, message_id=msg)
    except Exception as e:
        print(e)


