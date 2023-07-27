from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import CallbackQuery, Message
from market.lexicon.lexicon_ru import LEXICON
from market.keyboards.keyboard_utils import db_add_product, list_product_keyboard, delete_product_keyboard, start_keyboard
from market.database.database import storage, cursor, conn
from market.models.models import FSMFillForm
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


router: Router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    print(message.from_user.id)
    await message.answer(LEXICON['/start'], reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


# Этот хэндлер будет срабатывать на кнопку "Добавит/Добавление задачи"
@router.callback_query(Text(text='add'), StateFilter(default_state))
async def add_button_call(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON['write_product'])
    # Отправляем запрос на ожидание следующего сообщения от пользователя
    await state.set_state(FSMFillForm.add_product)


# Этот хэндлер будет срабатывать и переводить в состояние ожидания ввода продукта
@router.message(StateFilter(FSMFillForm.add_product))
async def add_task(message: Message, state: FSMContext):
    # Получаем введенную пользователем задачу
    product = message.text.lower()
    user_id = message.from_user.id
    db_add_product(user_id, product)
    await message.answer(LEXICON['agree'])

    # Сбрасываем состояние
    await state.clear()

    await message.answer(LEXICON['choose'], reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать на кнопку "Список задач"
@router.callback_query(Text(text='list'))
async def list_button_call(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Получаем все задачи с их статусами для данного пользователя из базы данных
    cursor.execute('SELECT id, product, done id FROM market WHERE user_id=?', (user_id,))
    products = cursor.fetchall()

    if products:
        product_keyboard = list_product_keyboard(products)
        await callback.message.answer(LEXICON['list'], reply_markup=product_keyboard)
    else:
        await callback.message.answer(LEXICON['not_products'], reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать когда нажали на одну из задач из списка
@router.callback_query(Text(startswith='done:'))
async def done_button_call(callback: CallbackQuery):
    # Получаем идентификатор задачи
    user_id = callback.from_user.id
    product_id = callback.data.split(':')[1]

    # Изменяем статус задачи на "Выполнено" в базе данных
    cursor.execute('UPDATE market SET done=? WHERE user_id=? AND id=?', ('да', user_id, product_id))
    conn.commit()

    await callback.message.answer(LEXICON['done_deal'], reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать на кнопку "home"
@router.callback_query(Text(text='home'))
async def home_command(callback: CallbackQuery):
    print(callback.from_user.id)
    await callback.message.answer(LEXICON['choose'], reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать на кнопку "Удалить"
@router.callback_query(Text(text='del'))
async def delete_button_call(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Получаем все задачи для данного пользователя из базы данных
    cursor.execute('SELECT id, product, done FROM market WHERE user_id=?', (user_id,))
    products = cursor.fetchall()

    if products:
        task_keyboard = delete_product_keyboard(products)
        await callback.message.answer(LEXICON['delete_products'], reply_markup=task_keyboard)
    else:
        await callback.message.answer(LEXICON['not_products'], reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать когда вы зашли в список для удалении и выбрали одну из задач
@router.callback_query(Text(startswith='del:'))
async def dell_button_call(callback: CallbackQuery):
    # Получаем идентификатор задачи
    task_id = callback.data.split(':')[1]

    # Удаляем задачу из базе данных
    cursor.execute('DELETE FROM market WHERE id=?', (task_id,))
    conn.commit()

    await callback.message.answer(LEXICON['del_deal'], reply_markup=start_keyboard)