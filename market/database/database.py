import sqlite3
from aiogram.fsm.storage.memory import MemoryStorage


# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()

# Соединение с базой данных
conn = sqlite3.connect('market.db', timeout=10)
cursor = conn.cursor()