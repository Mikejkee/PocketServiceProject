from django.db import transaction, IntegrityError
from datetime import datetime

from PocketServiceApp.models import Client, Role, Product, Administrator, Smeta, Order, Agent


head_admin_role = Role.objects.filter(role_type='Главный администратор').last()
head_admin = Administrator.objects.filter(role=head_admin_role).last()


def save_user(role_type=None, name=None, surname=None, patronymic=None, date_of_birth=None,
              phone_number=None, username=None, telegram_chat_id=None,
              telegram_id=None, telegram_username=None, telegram_name=None,
              telegram_surname=None, email=None, background_image=None, address=None,
              addition_information=None, object_information=None):

    with transaction.atomic():
        clients = Client.objects.filter(telegram_id=str(telegram_id))
        if clients.count() > 0:
            clients.update(name=name, surname=surname, patronymic=patronymic,
                           date_of_birth=date_of_birth, phone_number=phone_number,
                           username=username, telegram_chat_id=telegram_chat_id,
                           telegram_id=telegram_id, telegram_username=telegram_username,
                           telegram_name=telegram_name, telegram_surname=telegram_surname,
                           email=email, background_image=background_image, address=address,
                           addition_information=addition_information, object_information=object_information)
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


