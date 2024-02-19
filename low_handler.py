# low_handler.py
from site_API.api_request import get_actors
from telebot.types import Message
from typing import Any

def handle_low(bot: Any, message: Message) -> None:
    """
    Обработка команды /low.

    Запрашивает у пользователя количество актеров и устанавливает состояние пользователя для следующего ввода.
    """
    bot.send_message(message.chat.id, 'Введите количество актёров:')
    bot.register_next_step_handler(message, lambda m: handle_low_response(bot, m))

def handle_low_response(bot: Any, message: Message) -> None:
    """
    Обработка ответа пользователя на запрос количества актеров.

    Получает информацию о заданном количестве актеров и выводит ее в чат.
    """
    try:
        # Попытка преобразовать введенное количество актеров в число
        num_actors_to_display: int = int(message.text)

        # Получить информацию о заданном количестве актеров
        actors_info = get_actors(num_actors_to_display)

        if actors_info:
            # Вывести информацию в чат
            for actor in actors_info:
                actor_info = 'Имя: {}, Год рождения: {}, Год смерти: {}\nЗанятие: {}\n'.format(
                    actor['primaryName'], actor['birthYear'], actor['deathYear'], actor['primaryProfession'])
                bot.send_message(message.chat.id, actor_info)
        else:
            bot.send_message(message.chat.id, "Ошибка при запросе API.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число актёров.")
