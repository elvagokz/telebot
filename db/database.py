# database.py
from peewee import Model, SqliteDatabase, CharField, DateTimeField, SQL
from typing import List, Optional

# Инициализация SQLite базы данных и определение модели CommandHistory
db: SqliteDatabase = SqliteDatabase('commands.db')

class CommandHistory(Model):
    command: CharField = CharField()
    time: DateTimeField = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        database: SqliteDatabase = db

def initialize_database() -> None:
    """
    Инициализация базы данных.

    Подключается к базе данных и создает таблицу CommandHistory, если она не существует.
    """
    db.connect()
    db.create_tables([CommandHistory])

def save_command(command: str, user_id: Optional[int] = None) -> None:
    """
    Сохранение команды в базе данных.

    :param command: Команда, которую необходимо сохранить.
    :param user_id: Идентификатор пользователя (не используется в данной реализации).
    """
    CommandHistory.create(command=command)

def get_last_n_commands(n: int) -> List[CommandHistory]:
    """
    Получение последних N записей из истории команд.

    :param n: Количество записей для извлечения.
    :return: Список объектов CommandHistory, представляющих N последних команд.
    """
    return CommandHistory.select().order_by(CommandHistory.time.desc()).limit(n)

def close_database() -> None:
    """
    Закрытие соединения с базой данных.
    """
    db.close()
