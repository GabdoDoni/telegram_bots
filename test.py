from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text, CommandStart, StateFilter
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from dotenv import load_dotenv, find_dotenv
from aiogram.types import BotCommand
from aiogram.fsm.state import default_state
import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


# Для загрузки переменных из файла .env
load_dotenv(find_dotenv())

# Вместо API_TOKEN нужно вставить токен вашего бота, полученный у @BotFather
API_TOKEN: str = os.environ.get('API_TOKEN')

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Соединение с базой данных
conn = sqlite3.connect('test.db', check_same_thread=False)
cursor = conn.cursor()


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    add_task = State()        # Состояние ожидания ввода задачи


# Создаем объекты инлайн-кнопок
add_button: InlineKeyboardButton = InlineKeyboardButton(
    text='Добавление задачи',
    callback_data='add')
done_button: InlineKeyboardButton = InlineKeyboardButton(
    text='Добавить в список выполненых',
    callback_data='done')
delete_button: InlineKeyboardButton = InlineKeyboardButton(
    text='Удаление задачи',
    callback_data='delete')
list_button: InlineKeyboardButton = InlineKeyboardButton(
    text='Список задач',
    callback_data='list')
success_button: InlineKeyboardButton = InlineKeyboardButton(
    text='Список выполненных задач',
    callback_data='success')

# Создаем объект инлайн-клавиатуры
start_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[add_button],
                     [list_button],
                     [success_button]])

edit_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[add_button],
                     [delete_button]])


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    print(message.from_user.id)
    await message.answer('Привет!\nМеня зовут бот-список задач!\nМожете писать сюда ваши задачи'
                         '\n\n\nДля доступа большей информации напишите /help', reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать на кнопку "home"
@dp.callback_query(Text(text='home'))
async def home_command(callback: CallbackQuery):
    print(callback.from_user.id)
    await callback.message.answer('Выберите одну из функции', reply_markup=start_keyboard)


# Функция для добаление записи
def db_add_task(user_id: int, task: str):
    cursor.execute('INSERT INTO todo_list (user_id, task) VALUES (?, ?)', (user_id, task))
    conn.commit()


# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Для начало работы с ботом'),
        BotCommand(command='/help',
                   description='Справка по работе бота')]
    await bot.set_my_commands(main_menu_commands)


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer('Для начала работы телеграм бота напишите /start'
                         '\nДля добавлении новой задачи нажмите кнопку Добавить/Добавление задачи'
                         '\nДля вывода полного списка задач нажмите кнопку Список задач'
                         '\nДля вывода выполненых списков задач нажмите кнопку Список выполненых задач'
                         '\n\n\n'
                         '\nДля добавление в выполненые задачи нажмите задачу в списках'
                         '\nДля удаление одной задачи из списка нажмите кнопку Удалить и выберите одну задачу', reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать на кнопку "Добавит/Добавление задачи"
@dp.callback_query(Text(text='add'), StateFilter(default_state))
async def add_button_call(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Напиши задачу')
    # Отправляем запрос на ожидание следующего сообщения от пользователя
    await state.set_state(FSMFillForm.add_task)


# Этот хэндлер будет срабатывать и переводить в состояние ожидания ввода возраста
@dp.message(StateFilter(FSMFillForm.add_task))
async def add_task(message: Message, state: FSMContext):
    # Получаем введенную пользователем задачу
    task = message.text.lower()

    # Проверяем, существует ли уже задача у данного пользователя
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM todo_list WHERE user_id=? AND task=?', (user_id, task))
    existing_task = cursor.fetchone()

    if existing_task:
        await message.answer('У вас уже есть такая задача')
    else:
        # Добавляем задачу в базу данных
        db_add_task(user_id, task)
        await message.answer('Задача добавлена')

    # Сбрасываем состояние
    await state.clear()

    await message.answer('Выберите действие', reply_markup=start_keyboard)


# Функция для создания инлайн-клавиатуры с задачами
def list_task_keyboard(tasks: list) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Добавляем кнопки для каждой задачи
    for task in tasks:
        if task[2] == 'Не выполнено':
            task_id = task[0]
            kboard.row(InlineKeyboardButton(
                text=f'{task[1]}',
                callback_data=f'done:{task_id}'))
    # Добавляем в клавиатуру две кнопки "Добавить" и "Удалить"
    kboard.row(InlineKeyboardButton(
                    text='Добавить',
                    callback_data='add'),
               InlineKeyboardButton(
                    text='Удалить',
                    callback_data='delete'),
               width=2)
    # Добавляем в клавиатуру в конце кнопку "Назад"
    kboard.row(InlineKeyboardButton(
                    text='Назад',
                    callback_data='home'))

    return kboard.as_markup()


# Этот хэндлер будет срабатывать на кнопку "Список задач"
@dp.callback_query(Text(text='list'))
async def list_button_call(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Получаем все задачи с их статусами для данного пользователя из базы данных
    cursor.execute('SELECT id, task, status id FROM todo_list WHERE user_id=?', (user_id,))
    tasks = cursor.fetchall()

    if tasks:
        task_keyboard = list_task_keyboard(tasks)
        await callback.message.answer('Список задач:', reply_markup=task_keyboard)
    else:
        await callback.message.answer('У вас нет задач', reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать когда нажали на одну из задач из списка
@dp.callback_query(Text(startswith='done:'))
async def done_button_call(callback: CallbackQuery):
    # Получаем идентификатор задачи
    user_id = callback.from_user.id
    task_id = callback.data.split(':')[1]

    # Изменяем статус задачи на "Выполнено" в базе данных
    cursor.execute('UPDATE todo_list SET status=? WHERE user_id=? AND id=?', ('Выполнено', user_id, task_id))
    conn.commit()

    await callback.message.answer('Задача отмечена как выполненная.', reply_markup=start_keyboard)


# Функция для создания инлайн-клавиатуры для удаление из списка
def delete_task_keyboard(tasks: list) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Добавляем кнопки для каждой задачи

    for task in tasks:
        if task[2] == 'Не выполнено':
            task_id = task[0]
            kboard.row(InlineKeyboardButton(
                text=f'{task[1]}',
                callback_data=f'del:{task_id}'))
    # Добавляем в клавиатуру в конце кнопку "Назад"
    kboard.row(InlineKeyboardButton(
                    text='Назад',
                    callback_data='list'))

    return kboard.as_markup()


# Этот хэндлер будет срабатывать на кнопку "Удалить"
@dp.callback_query(Text(text='delete'))
async def delete_button_call(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Получаем все задачи для данного пользователя из базы данных
    cursor.execute('SELECT id, task, status FROM todo_list WHERE user_id=?', (user_id,))
    tasks = cursor.fetchall()

    if tasks:
        task_keyboard = delete_task_keyboard(tasks)
        await callback.message.answer('Задачи для удаления', reply_markup=task_keyboard)
    else:
        await callback.message.answer('У вас нет задач', reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать когда вы зашли в список для удалении и выбрали одну из задач
@dp.callback_query(Text(startswith='del:'))
async def dell_button_call(callback: CallbackQuery):
    # Получаем идентификатор задачи
    user_id = callback.from_user.id
    task_id = callback.data.split(':')[1]

    # Удаляем задачу из базе данных
    cursor.execute('DELETE FROM todo_list WHERE id=?', (task_id,))
    conn.commit()

    await callback.message.answer('Задача удалена.', reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def other_text_answers(message: Message):
    await message.answer('Пожалуйста вводите только в том случае, если вас попросят', reply_markup=start_keyboard)


# Функция для создания инлайн-клавиатуры со списком выполненых работ
def success_task_keyboard(tasks: list) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Добавляем кнопки для каждой задачи
    for task in tasks:
        if task[2] == 'Выполнено':
            kboard.row(InlineKeyboardButton(
                text=f'{task[1]}',
                callback_data='sucs'))
    # Добавляем в клавиатуру в конце кнопку "Назад"
    kboard.row(InlineKeyboardButton(
                    text='Назад',
                    callback_data='home'))

    return kboard.as_markup()


# Этот хэндлер будет срабатывать на кнопку "Список выполненых задач"
@dp.callback_query(Text(text='success'))
async def success_button_call(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Получаем все задачи с их статусами для данного пользователя из базы данных
    cursor.execute('SELECT id, task, status id FROM todo_list WHERE user_id=?', (user_id,))
    tasks = cursor.fetchall()

    if tasks:
        task_success_keyboard = success_task_keyboard(tasks)
        await callback.message.answer('Список выполненых задач:', reply_markup=task_success_keyboard)
    else:
        await callback.message.answer('У вас нет задач', reply_markup=start_keyboard)


# Этот хэндлер будет срабатывать когда вы выбрали одну из задач из выполненых задач
@dp.callback_query(Text(text='sucs'))
async def  sucs_button_call(callback: CallbackQuery):
    await callback.message.answer('Эту задачу вы уже выполнели', reply_markup=start_keyboard)


if __name__ == '__main__':
    # Регистрируем асинхронную функцию в диспетчере,
    # которая будет выполняться на старте бота,
    dp.startup.register(set_main_menu)
    # Запускаем поллинг
    dp.run_polling(bot)
