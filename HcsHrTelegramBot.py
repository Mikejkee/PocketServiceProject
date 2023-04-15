import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Text
from aiogram.filters.command import Command

# Логирование
logging.basicConfig(level=logging.INFO)

# Объект бота TODO: вынести в отдельный файл env-ы
TOKEN = "6138821594:AAEatK-fHgdQoHqNT-tSBX-DMk2T-MCRB14"

# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Ты попал в систему, которая в данный момент разрабатывается, напиши /command")


# Хэндлер на команду /start
@dp.message(Command("command"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Оформить заказ"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ оформления заказа"
    )
    await message.answer("Выбери нужную команду", reply_markup=keyboard)


@dp.message(Text("Оформить заказ"))
async def with_puree(message: types.Message):
    await message.reply("Скоро здесь будет вау!")


# Запуск процесса поллинга новых апдейтов
async def main():
    bot = Bot(token=TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
