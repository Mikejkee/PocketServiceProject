from celery import shared_task
from aiogram import Bot
import time
import asyncio

from mainmodule.celery import BaseTask
# from PocketServiceTelegramBot import TOKEN


@shared_task(base=BaseTask)
def save_client_task(name, surname, patronymic, person_fio, date_of_birth, phone_number, telegram_chat_id,
                     telegram_id, telegram_username, telegram_name, telegram_surname, email,
                     background_image, address, addition_information):

    from .controllers.bot_services import save_user
    print('Start delay')
    save_user('Клиент', name, surname, patronymic, person_fio, date_of_birth, phone_number,
              telegram_chat_id, telegram_id, telegram_username, telegram_name, telegram_surname,
              email, background_image, address, addition_information)

    return True


@shared_task(base=BaseTask)
def create_product_order_task(phone_number, telegram_chat_id, client_id, fio, email, address, addition_information,
                              agent_id, product_id, order_name, order_price, order_start_time, order_deadline,
                              order_information):

    from .controllers.bot_services import save_user, create_order
    save_user(phone_number=phone_number, telegram_chat_id=telegram_chat_id,
              telegram_id=client_id, person_fio=fio, email=email, address=address,
              addition_information=addition_information)

    order_id = create_order(client_id, agent_id, product_id, order_name, order_price, order_start_time,
                            order_deadline, order_information)

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


@shared_task(base=BaseTask)
def create_comment_task(comment_photos, agent_id, client_telegram_id, order_id, rating, comment_text):

    from .controllers.bot_services import create_comment

    comment_id = create_comment(comment_photos, agent_id, client_telegram_id, order_id, rating, comment_text)

    return comment_id


@shared_task(base=BaseTask)
def update_education_task(education_id, university_name, specialization_name, education_end):

    from .controllers.bot_services import update_education

    update_education(education_id, university_name, specialization_name, education_end)
