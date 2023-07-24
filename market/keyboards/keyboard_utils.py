from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from market.lexicon.lexicon_ru import LEXICON
# from market.services.services import book


# Создаем объекты инлайн-кнопок
add_button: InlineKeyboardButton = InlineKeyboardButton(
    text=LEXICON['add'],
    callback_data='add')
list_button: InlineKeyboardButton = InlineKeyboardButton(
    text=LEXICON['list'],
    callback_data='list')
delete_button: InlineKeyboardButton = InlineKeyboardButton(
    text='del',
    callback_data='del')


# Создаем объект инлайн-клавиатуры
start_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[add_button],
                     [list_button]])

edit_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[add_button],
                     [delete_button]])


def create_list_keyboard(*args: int) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    count = 1
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{count} - {button}',
            callback_data=str(button)))
        count += 1
    # Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    kb_builder.row(InlineKeyboardButton(
                        text=LEXICON['del'],
                        callback_data='del'),
                   InlineKeyboardButton(
                        text=LEXICON['cancel'],
                        callback_data='cancel'),
                   width=2)
    return kb_builder.as_markup()


def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{LEXICON["delete"]} - {button}',
            callback_data=f'{button}del'))
    # Добавляем в конец клавиатуры кнопку "Отменить"
    kb_builder.row(InlineKeyboardButton(
                        text=LEXICON['cancel'],
                        callback_data='cancel'))
    return kb_builder.as_markup()

