from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
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

# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 6

# Словарь, в котором будут храниться данные пользователя
users: dict = {}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    print(message.from_user.id)
    await message.answer('Привет!\nМеня зовут бот-загадка чисел!\nУгадываете число от 1 до 100\nХотите сыграть?'
                         '\n\n\nЕсли вам что-то непонятно напишите /help')
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('В этой игре я загадываю число от 0 до 100, а вы пытаетесь отгадать\nУ вас 6 попыток'
                         '\nЕсли ваше число больше или меньше моего, я буду подсказывать'
                         '\nПосле игр можете посмотреть статистику, напишите /stats')


# Этот хэндлер будет срабатывать на команду "/stats"
@dp.message(Command(commands=['stats']))
async def stats_users(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}
        await message.answer('Ваша cтатистика'
                         f'\nКоличество игр = {users[message.from_user.id]["total_games"]}'
                         f'\nКоличство побед = {users[message.from_user.id]["wins"]}')


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands=['cancel']))
async def cancel_game(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Игра закончена'
                             '\nХотите сыграть еще?')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('Мы еще не начали игру')


# Этот хэндлер для начала игры
@dp.message(Text(text=['Да', 'Начнем', 'Yes', 'Go', 'Evet'], ignore_case=True))
async def start_game(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}
        await message.answer('Игра начилась'
                             '\nугадай число')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        print(users[message.from_user.id]['secret_number'])
        users[message.from_user.id]['attempts'] = ATTEMPTS
    elif not users[message.from_user.id]['in_game']:
        await message.answer('Игра начилась'
                             '\nугадай число')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        print(users[message.from_user.id]['secret_number'])
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer('Игра уже играем')


# Этот хэндлер для отказа от игры
@dp.message(Text(text=['Нет', 'Стоп', 'No', 'Stop', 'Hayir'], ignore_case=True))
async def negative_answer(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}
        await message.answer('Мы не играем')
    elif not users[message.from_user.id]['in_game']:
        await message.answer('Хорошо, напишите если захотите сыграть')
    else:
        await message.answer('Мы же играем'
                             '\nЕсли хотите закончить напишите /cancel')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def what_number(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}
        await message.answer('Здорова бандиты, чтобы начать нажми да')
    elif users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number'] and users[message.from_user.id]['attempts'] > 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer('Ура!!! Вы угадали число!\n'
                                 f'Количество оставшихся попыток {users[message.from_user.id]["attempts"]}\n\n'
                                 'Может, сыграем еще?')

        elif int(message.text) > users[message.from_user.id]['secret_number'] and users[message.from_user.id]['attempts'] > 0:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Ваше число больше моего'
                                 f'\nОсталось попыток {users[message.from_user.id]["attempts"]}')

        elif int(message.text) < users[message.from_user.id]['secret_number'] and users[message.from_user.id]['attempts'] > 0:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Ваше число меньше моего'
                                 f'\nОсталось попыток {users[message.from_user.id]["attempts"]}')

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer('Вы проиграли'
                                 f'\nЗагаднное число {users[message.from_user.id]["secret_number"]} '
                                 f'\n\nЕсли хотите сыграть напишите')

    else:
        await message.answer('Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_text_answers(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}
        await message.answer('Здорова бандиты, чтобы начать нажми да')
    elif users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')


if __name__ == '__main__':
    dp.run_polling(bot)