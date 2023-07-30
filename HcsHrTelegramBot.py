import asyncio
from asgiref.sync import sync_to_async
import logging
from aiogram import F, Bot, Dispatcher, types
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram.types.web_app_info import WebAppInfo

from PocketServiceApp.telegram_tasks import save_client_task, create_product_order_task, tg_message_task, \
    update_product_order_task

# Логирование
logging.basicConfig(level=logging.INFO)

# Объект бота TODO: вынести в отдельный файл env-ы
TOKEN = "6138821594:AAEatK-fHgdQoHqNT-tSBX-DMk2T-MCRB14"
# CREW_URL = 'https://127.0.0.1:8000'
CREW_URL = 'web.pocket-service.ru'

# Диспетчер
dp = Dispatcher()

start_buttons = [
    [
        KeyboardButton(text='Личный кабинет 💼'),
        KeyboardButton(text='Витрина услуг 📜️'),
    ]
]

keyboard_start = ReplyKeyboardMarkup(
    keyboard=start_buttons,
    resize_keyboard=True
)


@sync_to_async
def save_client(name=None, surname=None, patronymic=None,
                date_of_birth=None, phone_number=None, username=None, telegram_chat_id=None,
                telegram_id=None, telegram_username=None, telegram_name=None,
                telegram_surname=None, email=None, background_image=None, address=None,
                addition_information=None, object_information=None):
    task = save_client_task.delay(name, surname, patronymic, date_of_birth, phone_number, username,
                                  telegram_chat_id, telegram_id, telegram_username, telegram_name,
                                  telegram_surname, email, background_image, address,
                                  addition_information, object_information)
    print('TASK CREATES - SAVE CLIENT ', task.task_id)


def tg_reminder(telegram_id, message, time=0):
    task = tg_message_task.apply_async(kwargs={'telegram_id': telegram_id, 'message': message, 'token': TOKEN},
                                       countdown=time)
    print('TASK CREATES - tg reminder ', task.task_id)
    return task.task_id


@sync_to_async
def create_product_order(phone_number, telegram_chat_id, client_id, email,
                         address, addition_information, object_information,
                         agent_id, product_type, product_addition_information,
                         order_name, order_price,
                         order_deadline, order_information):
    order_task = create_product_order_task.delay(phone_number, telegram_chat_id, client_id, email,
                                                 address, addition_information, object_information,
                                                 agent_id, product_type, product_addition_information,
                                                 order_name, order_price, order_deadline, order_information)
    print('TASK CREATES - create order ', order_task.task_id)

    client_remind_task = tg_reminder(client_id, "Вы зарегистрировали заявку на {} . \n"
                                                "Ожидайте, как с вами свяжется исполнитель".format(product_addition_information))
    print('TASK CREATES - client remind ', client_remind_task)

    agent_remind_task = tg_reminder(agent_id, "Вам пришла заявка на {}, \n "
                                              "Свяжитесь с заказчиком. \n"
                                              "Телефон: {} , email: {}".format(product_addition_information,
                                                                                phone_number, email))
    print('TASK CREATES - agent remind ', agent_remind_task)

    agent_remind_task = tg_reminder(agent_id, "Напоминанем, что вам пришла заявка на {}, \n "
                                              "Свяжитесь с заказчиком и отметьте  в личном "
                                              "кабинете ифнормацию о принятии заказа. \n"
                                              "Телефон: {} , email: {}".format(product_addition_information,
                                                                                phone_number, email),
                                    10)
    print('TASK CREATES - agent remind 3h ', agent_remind_task)

    update_order_task = update_product_order_task.delay(order_id=order_task.get(), reminder_status=1)
    print('TASK CREATES - update order', update_order_task.task_id)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    chat = message.chat
    chat_id = chat.id

    from_user = message.from_user
    telegram_id = from_user.id
    telegram_username = from_user.username
    telegram_name = from_user.first_name
    telegram_surname = from_user.last_name

    hello = f'Добро пожаловать в нашу систему поиска специалиста!'
    if not telegram_username:
        if telegram_name:
            hello = f'<b>{telegram_name}</b>, приветствуем тебя!'
        elif not telegram_name and telegram_surname:
            hello = f'<b>{telegram_surname}</b>, приветствуем тебя!'
    else:
        hello = f'<b>{telegram_username}</b>, приветствуем тебя!'

    hcs_user = await save_client(telegram_chat_id=chat_id, telegram_id=telegram_id,
                                 telegram_name=telegram_name, telegram_surname=telegram_surname,
                                 telegram_username=telegram_username)

    await message.answer(f'{hello}\n\n'
                         'У тебя что-то сломалось? Тебе надо сделать ремонт? Ищешь мастера? \n\n'
                         '<b>Личный кабинет</b> 💼 - для просмотра информации о своем объекте.\n'
                         '<b>Витрина услуг </b> 📜 - здесь можно заказать ремонт квартиры, сантехники, '
                         'найти мастера по маникюру, бровям.\n'
                         '',
                         reply_markup=keyboard_start,
                         parse_mode='HTML')


@dp.message(Text('🔙 Главное меню'))
async def flat_repair(message: Message):
    await message.answer('Выберите необходимое',
                         reply_markup=keyboard_start,
                         parse_mode='HTML')


@dp.message(Text("Витрина услуг 📜️"))
async def showcase(message: Message):
    chat = message.chat
    telegram_chat_id = chat.id

    from_user = message.from_user
    client_id = from_user.id

    # Пример работы заказа сметчика
    # await create_product_order('8802553535', telegram_chat_id, client_id, 'maikl.kurpatov@yandex.ru',
    #                            'address', 'addition_information', 'object_information',
    #                            '5721238199', 0, 'Заказать сметчика',
    #                            'Первый заказ тест', '50000', '2023-07-07', 'Первый заказ сметчика')

    webapp_data = message.web_app_data

    if not webapp_data:
        webApp_flat_repair = WebAppInfo(
            url=f'{CREW_URL}/PocketServiceApp/showcase/?TelegramId={client_id}&ShowcaseType=0')
        button_0 = KeyboardButton(text='Ремонт квартиры', web_app=webApp_flat_repair)

        webApp_technique_repair = WebAppInfo(
            url=f'{CREW_URL}/PocketServiceApp/showcase/?TelegramId={client_id}&ShowcaseType=1')
        button_1 = KeyboardButton(text='Ремонт техники', web_app=webApp_technique_repair)

        webApp_furniture_repair = WebAppInfo(
            url=f'{CREW_URL}/PocketServiceApp/showcase/?TelegramId={client_id}&ShowcaseType=2')
        button_2 = KeyboardButton(text='Ремонт мебели', web_app=webApp_furniture_repair)

        webApp_beauty_services = WebAppInfo(
            url=f'{CREW_URL}/PocketServiceApp/showcase/?TelegramId={client_id}&ShowcaseType=2')
        button_3 = KeyboardButton(text='Услуги красоты', web_app=webApp_beauty_services)

        button_back = KeyboardButton(text='🔙 Главное меню')

        buttons = [
            [
                button_0,
                button_1,
            ],
            [
                button_2,
                button_3,
            ],
            [
                button_back,
            ],
        ]

        keyboard_showcase = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

        await message.answer(f'Выбери:\n\n'
                             f'<b>Ремонт квартиры</b> - если хочешь заказать бригаду для ремонта квартиры\n'
                             f'<b>Ремонт техники</b> - найти рабочего для ремонта техники\n'
                             f'<b>Ремонт мебели</b> - найти рабочего для ремонта мебели.\n'
                             f'<b>Услуги красоты</b> - поиск мастеров маникюра, педикюра, бровей и т.д.\n'
                             f'',
                             reply_markup=keyboard_showcase,
                             parse_mode='HTML')


# Запуск процесса поллинга новых апдейтов
async def main():
    bot = Bot(token=TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
