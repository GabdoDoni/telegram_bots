import os

from environs import Env

env = Env()
env.read_env()

print(env('BOT_TOKEN'))
print(env('ADMIN_ID'))