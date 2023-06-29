from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str                   # название базы данных
    db_host: str                    # url-адрес базы данных
    db_user: str                    # username пользователя базы данных
    db_password: str                # пароль к базы данных


@dataclass
class TgBot:
    token: str                      # токен для доступа к тг-боту
    admin_ids: list[int]            # список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


# Создаем экземпляр класса Env
env: Env = Env()

# Добавляем в переменную окружения данные из файла .env
env.read_env()

# Создаем экземпляр класса Config и наполняем данными
config = Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                             admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                db=DatabaseConfig(database=env('DATABASE'),
                                  db_host=env('DB_HOST'),
                                  db_user=env('DB_USER'),
                                  db_password=env('DB_PASSWORD')))

# Выводим на печать, чтобы проверить
print('BOT_TOKEN:', config.tg_bot.token)
print('ADMIN_IDS:', config.tg_bot.admin_ids)

print('DATABASE:', config.db.database)
print('DB_HOST:', config.db.db_host)
print('DB_USER:', config.db.db_user)
print('DB_PASSWORD:', config.db.db_password)

