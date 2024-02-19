# loader.py
import telebot
from dotenv import load_dotenv
import os
from db.database import initialize_database, save_command, close_database, get_last_n_commands
from high_handler import handle_high
from low_handler import handle_low
from custom_handler import handle_custom

load_dotenv()

TOKEN = os.getenv("TOKEN")

initialize_database()

bot = telebot.TeleBot(TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])

def handle_start(message: telebot.types.Message) -> None:
    """
        Обработка команды /start.

        Выводит приветственное сообщение и инструкции по использованию бота.
        """
    start_message = """
    Добрый день, это бот, посвященный актерам.

    У меня Вы можете узнать:

    Годы рождения самых молодых из них командой /low,
    Годы рождения самых старых командой /high,
    Или узнать кто родился в заданном промежутке /custom.
    Если хочешь вспомнить историю запросов, то введи /history
    """
    bot.send_message(message.chat.id, start_message)

# Команда /help
@bot.message_handler(commands=['help'])
def handle_help(message: telebot.types.Message) -> None:
    """
        Обработка команды /help.

        Выводит список доступных команд и их описания.
        """
    help_message = """
    Доступные команды:
    /low - годы рождения самых молодых из них командой;
    /high - годы рождения самых старых командой;
    /custom - узнать кто родился в заданном промежутке;
    /history - вывести историю запросов.
    """
    bot.send_message(message.chat.id, help_message)

# Команда /low
@bot.message_handler(commands=['low'])
def handle_low_command(message: telebot.types.Message) -> None:
    """
        Обработка команды /low.

        Вызывает функцию handle_low и сохраняет команду в базе данных.
        """
    handle_low(bot, message)
    save_command(message.text, message.from_user.id)

# Команда /high
@bot.message_handler(commands=['high'])
def handle_high_command(message: telebot.types.Message) -> None:
    """
        Обработка команды /high.

        Вызывает функцию handle_high и сохраняет команду в базе данных.
        """
    handle_high(bot, message)
    save_command(message.text, message.from_user.id)

# Команда /custom
@bot.message_handler(commands=['custom'])
def handle_custom_command(message: telebot.types.Message) -> None:
    """
        Обработка команды /custom.

        Вызывает функцию handle_custom и сохраняет команду в базе данных.
        """
    handle_custom(message, bot)
    save_command(message.text, message.from_user.id)


@bot.message_handler(commands=['history'])
def handle_history(message: telebot.types.Message) -> None:
    """
        Обработка команды /history.

        Получает последние 5 записей о командах из базы данных и отправляет их в качестве ответа.
        """
    history_entries = get_last_n_commands(5)
    if history_entries:
        response = "Последние 5 команд:\n"
        for entry in history_entries:
            response += 'Команда: {}, Время: {}\n'.format(entry.command, entry.time)
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "История команд пуста.")


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message: telebot.types.Message) -> None:
    """
        Обработка текстовых сообщений.

        Реагирует на определенные текстовые сообщения, такие как 'привет', и предоставляет общее сообщение для других случаев.
        """
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'И тебе привет, добрый человек!')
    else:
        bot.send_message(message.chat.id, 'Извините, я пока не понимаю ваш запрос. Если запутался, введи /help')

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    finally:
        close_database()
