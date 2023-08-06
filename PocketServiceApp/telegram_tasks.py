from celery import shared_task
from aiogram import Bot
import time
import asyncio

from mainmodule.celery import BaseTask
# from PocketServiceTelegramBot import TOKEN


@shared_task(base=BaseTask)
def save_client_task(name, surname, patronymic,date_of_birth, phone_number, username, telegram_chat_id,
                     telegram_id, telegram_username, telegram_name, telegram_surname, email,
                     background_image, address, addition_information, object_information):

    from .controllers.bot_services import save_user
    print('Start delay')
    save_user('Обычный клиент', name, surname, patronymic, date_of_birth, phone_number, username,
              telegram_chat_id, telegram_id, telegram_username, telegram_name, telegram_surname,
              email, background_image, address, addition_information, object_information)

    return True


@shared_task(base=BaseTask)
def create_product_order_task(phone_number, telegram_chat_id, client_id, email,
                              address, addition_information, object_information,
                              agent_id, product_type, product_addition_information,
                              order_name, order_price, order_deadline, order_information):

    from .controllers.bot_services import save_user, create_order
    save_user(phone_number=phone_number, telegram_chat_id=telegram_chat_id,
              telegram_id=client_id, email=email, address=address,
              addition_information=addition_information, object_information=object_information)

    order_id = create_order(client_id, agent_id, product_type, product_addition_information,
                            order_name, order_price, order_deadline, order_information)

    return order_id


@shared_task(base=BaseTask)
def update_product_order_task(order_id, reminder_status=None, control_flag=None):

    from .controllers.bot_services import update_order
    update_order(order_id, reminder_status, control_flag)


@shared_task(base=BaseTask)
def tg_message_task(telegram_id, message, token):

    from .controllers.bot_services import tg_message
    bot = Bot(token=token, parse_mode="HTML")
    asyncio.run(tg_message(bot, telegram_id, message))

    return True

