from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from market.lexicon.lexicon_ru import LEXICON
from market.database.database import cursor, conn


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


# Функция для добаление записи
def db_add_product(user_id: int, product: str):
    cursor.execute('INSERT INTO market (user_id, product) VALUES (?, ?)', (user_id, product))
    conn.commit()


# Функция для создания инлайн-клавиатуры с задачами
def list_product_keyboard(products: list) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Добавляем кнопки для каждой задачи
    for product in products:
        print(product)
        if product[2] == 'нет':
            product_id = product[0]
            kboard.row(InlineKeyboardButton(
                text=f'{product[1]}',
                callback_data=f'done:{product_id}'))
    # Добавляем в клавиатуру две кнопки "Добавить" и "Удалить"
    kboard.row(InlineKeyboardButton(
                    text='Добавить',
                    callback_data='add'),
               InlineKeyboardButton(
                    text='Удалить',
                    callback_data='del'),
               width=2)
    # Добавляем в клавиатуру в конце кнопку "Назад"
    kboard.row(InlineKeyboardButton(
                    text='Назад',
                    callback_data='home'))
    return kboard.as_markup()


# Функция для создания инлайн-клавиатуры для удаление из списка
def delete_product_keyboard(products: list) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Добавляем кнопки для каждой задачи
    for product in products:
        print(product)
        if product[2] == 'нет':
            product_id = product[0]
            kboard.row(InlineKeyboardButton(
                text=f'{product[1]}',
                callback_data=f'del:{product_id}'))
    # Добавляем в клавиатуру в конце кнопку "Назад"
    kboard.row(InlineKeyboardButton(
                    text='Назад',
                    callback_data='list'))

    return kboard.as_markup()
