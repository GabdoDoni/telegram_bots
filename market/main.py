import os

from environs import Env

from config_data.config import load_config

env = Env()
env.read_env()

config = load_config('.env')


# Выводим на печать, чтобы проверить
print('BOT_TOKEN:', config.tg_bot.token)
print('ADMIN_IDS:', config.tg_bot.admin_ids)

print('DATABASE:', config.db.database)
print('DB_HOST:', config.db.db_host)
print('DB_USER:', config.db.db_user)
print('DB_PASSWORD:', config.db.db_password)