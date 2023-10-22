import asyncio
import os
import time
from pprint import pprint

import django
from asgiref.sync import sync_to_async
import logging
from aiogram import F, Bot, Dispatcher, types, Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram.types.web_app_info import WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainmodule.settings")
django.setup()

from PocketServiceApp.telegram_tasks import save_client_task, create_product_order_task, tg_message_task, \
    update_product_order_task, create_comment_task
from PocketServiceApp.models import Person, Client, Agent, Order

# Логирование
logging.basicConfig(level=logging.INFO)

rating_list = ['1 ⭐', '2 ⭐', '3 ⭐', '4 ⭐', '5 ⭐']

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CREW_URL = 'web.pocket-service.ru'
router = Router()
storage = RedisStorage.from_url(os.environ.get('CELERY_BACKEND'))


class CommentState(StatesGroup):
    choosing_agent = State()
    choosing_order = State()
    choosing_rating = State()
    choosing_comment_text = State()
    choosing_photo = State()


@sync_to_async
def get_agents_list():
    return Agent.objects.all().__str__()


agents_list = asyncio.run(get_agents_list())

@sync_to_async
def save_client(name=None, surname=None, patronymic=None, person_fio=None,
                date_of_birth=None, phone_number=None, telegram_chat_id=None,
                telegram_id=None, telegram_username=None, telegram_name=None,
                telegram_surname=None, email=None, background_image=None, address=None,
                addition_information=None):
    task = save_client_task.delay(name, surname, patronymic, person_fio, date_of_birth, phone_number,
                                  telegram_chat_id, telegram_id, telegram_username, telegram_name,
                                  telegram_surname, email, background_image, address,
                                  addition_information)
    print('TASK CREATES - SAVE CLIENT ', task.task_id)


def tg_reminder(telegram_id, message, time=0):
    task = tg_message_task.apply_async(kwargs={'telegram_id': telegram_id, 'message': message, 'token': TOKEN},
                                       countdown=time)
    print('TASK CREATES - tg reminder ', task.task_id)
    return task.task_id


@sync_to_async
def create_product_order(phone_number, telegram_chat_id, client_id, email,
                         address, addition_information,
                         agent_id, product_type, product_addition_information,
                         order_name, order_price,
                         order_deadline, order_information):
    order_task = create_product_order_task.delay(phone_number, telegram_chat_id, client_id, email,
                                                 address, addition_information,
                                                 agent_id, product_type, product_addition_information,
                                                 order_name, order_price, order_deadline, order_information)
    print('TASK CREATES - create order ', order_task.task_id)

    client_remind_task = tg_reminder(client_id, "Вы зарегистрировали заявку на {} . \n"
                                                "Ожидайте, как с вами свяжется исполнитель".format(
        product_addition_information))
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


@sync_to_async
def agents_list_from_orders_client(telegram_id):
    client_id = Client.objects.filter(telegram_id=telegram_id).last().id
    agents_id_list = Order.objects.filter(client_id=client_id).values_list('agent_id').distinct()
    agents_tg_list = []
    for agent_id in agents_id_list:
        agents_tg_list.append(Agent.objects.filter(id=agent_id[0]).last().__str__())
    return agents_tg_list


@sync_to_async
def comment_menu_agents_buttons(agents_list):
    buttons = []
    for agent in agents_list:
        buttons.append(
            [
                KeyboardButton(text=agent)
            ]
        )
    buttons.append([
        KeyboardButton(text='🔙 Главное меню')
    ])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


@sync_to_async
def comment_menu_orders_buttons(agent, client_tg):
    client = Client.objects.filter(telegram_id=client_tg).last().id
    orders = Order.objects.filter(agent_id=agent, client_id=client)

    buttons = []
    for order in orders:
        buttons.append(
            [
                KeyboardButton(text=str(order))
            ]
        )
    buttons.append([
        KeyboardButton(text='🔙 Главное меню')
    ])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


@sync_to_async
def user_check_status(telegram_id):
    user = Person.objects.filter(telegram_id=str(telegram_id))
    if user.count() > 0:
        return user.role.last().role_type
    else:
        return False


@sync_to_async
def start_menu_buttons(telegram_id):
    webApp_lc_user = WebAppInfo(url=f'https://{CREW_URL}/PocketServiceApp/profile/?TelegramId={telegram_id}')
    buttons = [
        [
            KeyboardButton(text='Личный кабинет 💼', web_app=webApp_lc_user),
            KeyboardButton(text='Витрина услуг 📜️'),
        ],
        [
            KeyboardButton(text='Выставить свои услуги 📞'),
            KeyboardButton(text='Оставить отзыв 💬'),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


@sync_to_async
def create_comment(comment_data, telegram_id):
    order_id = comment_data['order'].split('[')[1][:-1]
    print(comment_data)

    comment_images = []
    for i in range(1, int(comment_data['photo_counter']) + 1):
        comment_images.append(comment_data[f'comment_photo_{i}'])
    print(comment_images)

    comment_task = create_comment_task.delay(comment_images, comment_data['agent'], telegram_id, order_id,
                                             comment_data['rating'], comment_data['comment_text'])
    print('TASK CREATES - create comment ', comment_task.task_id)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

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

    await save_client(telegram_chat_id=chat_id, telegram_id=telegram_id, telegram_name=telegram_name,
                      telegram_surname=telegram_surname, telegram_username=telegram_username)

    keyboard = await start_menu_buttons(telegram_id)

    await message.answer(f'{hello}\n\n'
                         'У тебя что-то сломалось? Тебе надо сделать ремонт? Ищешь мастера? \n\n'
                         '<b>Личный кабинет</b> 💼 - для просмотра информации о своем объекте.\n'
                         '<b>Витрина услуг </b> 📜 - здесь можно заказать ремонт квартиры, сантехники, '
                         'найти мастера по маникюру, бровям.\n'
                         '<b>Связаться с нами </b> 📞 - если хочешь стать агентом, сотрудничать с нами или нашел '
                         'баги там ты найдешь наши контакты\n'
                         '<b>Оставить отзыв </b> 💬 - если хочешь оставить отзыв об агенте',
                         reply_markup=keyboard,
                         parse_mode='HTML')


@router.message(Text('🔙 Главное меню'))
async def head_menu(message: Message, state: FSMContext):
    from_user = message.from_user
    telegram_id = from_user.id
    keyboard = await start_menu_buttons(telegram_id)

    await state.clear()
    await message.answer('Выберите необходимое',
                         reply_markup=keyboard,
                         parse_mode='HTML')


@router.message(Text("Витрина услуг 📜️"))
async def showcase(message: Message):
    chat = message.chat
    telegram_chat_id = chat.id

    from_user = message.from_user
    client_id = from_user.id

    # Пример работы заказа сметчика
    # await create_product_order('8802553535', telegram_chat_id, client_id, 'maikl.kurpatov@yandex.ru',
    #                            'address', 'addition_information',
    #                            '5721238199', 0, 'Заказать сметчика',
    #                            'Первый заказ тест', '50000', '2023-07-07', 'Первый заказ сметчика')

    webapp_data = message.web_app_data

    if not webapp_data:
        webApp_flat_repair = WebAppInfo(
            url=f'https://{CREW_URL}/PocketServiceApp/showcase/?TelegramId={client_id}&ShowcaseType=0')
        button_0 = KeyboardButton(text='Ремонт квартиры', web_app=webApp_flat_repair)

        webApp_technique_repair = WebAppInfo(
            url=f'https://{CREW_URL}/PocketServiceApp/showcase/?TelegramId={client_id}&ShowcaseType=1')
        button_1 = KeyboardButton(text='Ремонт техники', web_app=webApp_technique_repair)

        webApp_furniture_repair = WebAppInfo(
            url=f'https://{CREW_URL}/PocketServiceApp/showcase/?TelegramId={client_id}&ShowcaseType=2')
        button_2 = KeyboardButton(text='Ремонт мебели', web_app=webApp_furniture_repair)

        webApp_beauty_services = WebAppInfo(
            url=f'https://{CREW_URL}/PocketServiceApp/showcase/?TelegramId={client_id}&ShowcaseType=3')
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


@router.message(Text('Выставить свои услуги 📞'))
async def contact_menu(message: Message):
    from_user = message.from_user
    telegram_id = from_user.id
    keyboard = await start_menu_buttons(telegram_id)

    await message.answer(f'Наши контакты:\n\n'
                         f'agent@web.pocket-service.ru - пиши, если хочешь стать новым агентом, в заявке обязательно '
                         f'нужно указать имя пользователя телеграмм @telegram_username или id, основную информацию '
                         f'о себе, название компании на которую вы работаете (если вы управляющий - укажите это). При '
                         f'этом если вы новая компания, которая хочет работать с нами - дополнительно предоставьте '
                         f'информацию о ней (ИНН, ОГРНИП, юридический адрес). Приложите все удостоверяющие личность '
                         f'и компанию документы, примеры ваших работ (профиль в профи.ру), информацию о заказах, '
                         f'отзывы и все, что вы считаете необходимым, чтоб было в вашем профиле. \n\n'
                         f'company@web.pocket-service.ru - пишите, если хотите зарегистировать вашу компанию у нас '
                         f'и сотрудничать, приложите описанные выше документы и информацию.\n\n'
                         f'bug@web.pocket-service.ru - пишите, заметите ошибки и баги в работе бота.\n\n'
                         f'Мы обязательно свяжемся с  вами! Ваш, Pocket Service.',
                         reply_markup=keyboard,
                         parse_mode='HTML')


@router.message(Text('Оставить отзыв 💬'))
async def comment_menu(message: Message, state: FSMContext):
    from_user = message.from_user
    telegram_id = from_user.id

    agents_tg_list = await agents_list_from_orders_client(telegram_id)
    keyboard = await comment_menu_agents_buttons(agents_tg_list)

    await message.answer(f'Какому агенту вы бы хотели оставить свой комментарий?', reply_markup=keyboard,
                         parse_mode='HTML')
    await state.set_state(CommentState.choosing_agent)


@sync_to_async
def agent_finder(message):
    agent_info = message.split('@')
    if isinstance(agent_info, list):
        return Agent.objects.filter(telegram_username=agent_info[1][:-1]).last().id
    else:
        return Agent.objects.filter(person_fio=agent_info).last().id


@router.message(CommentState.choosing_agent, F.text.in_(agents_list))
async def agent_chosen(message: Message, state: FSMContext):
    from_user = message.from_user
    telegram_id = from_user.id

    agent = await agent_finder(message.text)
    await state.update_data(agent=agent)
    await state.update_data(photo_counter=0)

    keyboard = await comment_menu_orders_buttons(agent, telegram_id)

    await message.answer(
        text="Теперь, выберите заказ, который вы хотите прокомментировать",
        reply_markup=keyboard
    )
    await state.set_state(CommentState.choosing_order)


@router.message(CommentState.choosing_agent)
async def agent_chosen_incorrectly(message: Message):
    await message.answer(
        text="Такого агента не существует.\n\n"
             "Пожалуйста, выберите из списка ниже:",
    )


@router.message(CommentState.choosing_order)
async def order_chosen(message: Message, state: FSMContext):
    await state.update_data(order=message.text)

    buttons = [
        [
            KeyboardButton(text=rating_list[0]),
            KeyboardButton(text=rating_list[1]),
        ],
        [
            KeyboardButton(text=rating_list[2]),
            KeyboardButton(text=rating_list[3]),
        ],
        [
            KeyboardButton(text=rating_list[4]),
        ],
        [
            KeyboardButton(text='🔙 Главное меню')
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await message.answer(
        text="Выберите оценку",
        reply_markup=keyboard
    )
    await state.set_state(CommentState.choosing_rating)


@router.message(CommentState.choosing_rating, F.text.in_(rating_list))
async def rating_chosen(message: Message, state: FSMContext):
    await state.update_data(rating=message.text.split(' ')[0])

    buttons = [
        [
            KeyboardButton(text='Совсем не понравилось'),
            KeyboardButton(text='Не понравилось'),
        ],
        [
            KeyboardButton(text='Пойдет'),
            KeyboardButton(text='Понравилось'),
        ],
        [
            KeyboardButton(text='Все понравилось'),
        ],
        [
            KeyboardButton(text='🔙 Главное меню')
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await message.answer(
        text="Теперь, пожалуйста, напишите свой комментарий к заказу, либо выберите в меню.",
        reply_markup=keyboard
    )
    await state.set_state(CommentState.choosing_comment_text)


@router.message(CommentState.choosing_rating)
async def rating_chosen_incorrectly(message: Message):
    buttons = [
        [
            KeyboardButton(text=rating_list[0]),
            KeyboardButton(text=rating_list[1]),
        ],
        [
            KeyboardButton(text=rating_list[2]),
            KeyboardButton(text=rating_list[3]),
        ],
        [
            KeyboardButton(text=rating_list[4]),
        ],
        [
            KeyboardButton(text='🔙 Главное меню')
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await message.answer(
        text="Такой оценки нет. Пожалуйста, выберите из списка ниже:",
        reply_markup=keyboard
    )


@router.message(CommentState.choosing_comment_text)
async def comment_chosen(message: Message, state: FSMContext):
    await state.update_data(comment_text=message.text)

    buttons = [
        [
            KeyboardButton(text='Нет'),
            KeyboardButton(text='Все'),
        ],
        [
            KeyboardButton(text='🔙 Главное меню')
        ],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await message.answer(
        text="Теперь, пожалуйста, приложитее фото к комментарию (если они отсутствуют - напишите «Нет»). \n"
             "Можно скидывать фото по одному, можно все сразу, если фото закончились - напишите «Все»",
        reply_markup=keyboard
    )
    await state.set_state(CommentState.choosing_photo)


@router.message(CommentState.choosing_photo)
async def photos_chosen(message: Message, state: FSMContext, bot: Bot):
    from_user = message.from_user
    telegram_id = from_user.id

    if message.content_type == 'photo':
        photo = message.photo[-1]
        time.sleep(1)
        photo_file = await bot.get_file(photo.file_id)
        photo_path = photo_file.file_path
        destination = f"/postgres_data/objects/comments/images/{photo.file_unique_id}.jpg"
        await bot.download_file(photo_path, f'./media{destination}')

        user_data = await state.get_data()
        photo_counter = user_data['photo_counter'] + 1

        await state.update_data({
            f'comment_photo_{photo_counter}': destination,
            'photo_counter': photo_counter,
        })
    else:
        keyboard = await start_menu_buttons(telegram_id)

        user_data = await state.get_data()
        await create_comment(user_data, telegram_id)

        await message.answer(
            text="Благодарим за комментарий!",
            reply_markup=keyboard
        )
        await state.clear()


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


async def main():
    bot = Bot(token=TOKEN, parse_mode="HTML")

    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
