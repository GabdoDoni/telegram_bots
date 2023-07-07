from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str                      # токен для доступа к тг-боту
    admin_ids: list[int]            # список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None) -> Config:

    # Создаем экземпляр класса Env
    env: Env = Env()

    # Добавляем в переменную окружения данные из файла .env
    env.read_env()

    # Создаем экземпляр класса Config и наполняем данными
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=list(map(int, env.list('ADMIN_IDS')))))




