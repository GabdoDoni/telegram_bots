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


def load_config(path: str | None = None) -> Config:

    # Создаем экземпляр класса Env
    env: Env = Env()

    # Добавляем в переменную окружения данные из файла .env
    env.read_env(path)

    # Создаем экземпляр класса Config и наполняем данными
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                  db=DatabaseConfig(database=env('DATABASE'),
                                    db_host=env('DB_HOST'),
                                    db_user=env('DB_USER'),
                                    db_password=env('DB_PASSWORD')))




