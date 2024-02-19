# custom_handler.py
import telebot
from site_API.api_request import get_actors_custom_years
from telebot.types import Message

def handle_custom(message: Message, bot: telebot.TeleBot) -> None:
    """
    Обработка команды /custom.

    Ожидает ввод начального года рождения от пользователя.
    """
    bot.send_message(message.chat.id, 'Введите начальный год рождения (гггг):')
    bot.register_next_step_handler(message, handle_custom_start_year, bot)

def handle_custom_start_year(message: Message, bot: telebot.TeleBot) -> None:
    """
    Обработка введенного пользователем начального года рождения.

    Ожидает ввод конечного года рождения от пользователя.
    """
    try:
        start_year = int(message.text)
        bot.send_message(message.chat.id, 'Введите конечный год рождения (гггг):')
        bot.register_next_step_handler(message, handle_custom_end_year, start_year, bot)
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный формат года. Пожалуйста, введите корректный год (гггг).')

def handle_custom_end_year(message: Message, start_year: int, bot: telebot.TeleBot) -> None:
    """
    Обработка введенного пользователем конечного года рождения.

    Выводит информацию о актерах, рожденных в заданном диапазоне годов.
    """
    try:
        end_year = int(message.text)
        if end_year < start_year:
            bot.send_message(message.chat.id, 'Конечный год должен быть не раньше начального года. Пожалуйста, введите корректные года.')
            return
        actors_info = get_actors_custom_years(start_year, end_year)
        if actors_info:
            for actor in actors_info:
                actor_info = f"Имя: {actor['primaryName']}, Год рождения: {actor['birthYear']}, Год смерти: {actor['deathYear']}\nЗанятие: {actor['primaryProfession']}\n"
                bot.send_message(message.chat.id, actor_info)
        else:
            bot.send_message(message.chat.id, f"Нет данных об актерах в заданном диапазоне годов.")
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный формат года. Пожалуйста, введите корректный год (гггг).')
