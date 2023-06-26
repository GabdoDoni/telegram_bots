from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text, BaseFilter
from aiogram.types import Message
import os
from dotenv import load_dotenv, find_dotenv
import random

load_dotenv(find_dotenv())

# Вместо API_TOKEN нужно вставить токен вашего бота, полученный у @BotFather
API_TOKEN: str = os.environ.get('API_TOKEN')


# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

admin: list[int] = [514897300]


class IsAdmin(BaseFilter):
    def __init__(self, admin: list[int]):
        self.admin = admin

    async def __call__(self, message: Message):
        return message.from_user.id in self.admin


# Этот хэндлер будет срабатывать, если апдейт от админа
@dp.message(IsAdmin(admin))
async def its_admin(message: Message):
    await message.answer(text='Its admin')


# Этот хэндлер будет срабатывать, если апдейт от админа
@dp.message()
async def messag(message: Message):
    await message.answer(text='NO admin')


if __name__ == '__main__':
    dp.run_polling(bot)