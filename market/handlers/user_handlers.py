from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from market.database.database import user_dict_template, users_db
from market.lexicon.lexicon_ru import LEXICON
from market.keyboards.keyboard_utils import create_list_keyboard, create_edit_keyboard, start_keyboard

router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON['/start'], reply_markup=start_keyboard)
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])


# Этот хэндлер будет срабатывать на команду "/list"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@router.message(Command(commands='list'))
async def process_beginning_command(message: Message):
    if users_db[message.from_user.id]["list"]:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_list_keyboard(
                *users_db[message.from_user.id]["list"]))
    else:
        await message.answer(text=LEXICON['no_list'])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()