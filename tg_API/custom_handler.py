# custom_handler.py
import api_request

def handle_custom(message, bot):
    bot.send_message(message.chat.id, 'Введите начальный год рождения (гггг):')
    bot.register_next_step_handler(message, handle_custom_start_year, bot)

def handle_custom_start_year(message, bot):
    try:
        start_year = int(message.text)
        bot.send_message(message.chat.id, 'Введите конечный год рождения (гггг):')
        bot.register_next_step_handler(message, handle_custom_end_year, start_year, bot)
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный формат года. Пожалуйста, введите корректный год (гггг).')

def handle_custom_end_year(message, start_year, bot):
    try:
        end_year = int(message.text)
        if end_year < start_year:
            bot.send_message(message.chat.id, 'Конечный год должен быть не раньше начального года. Пожалуйста, введите корректные года.')
            return
        actors_info = api_request.get_actors_custom_years(start_year, end_year)
        if actors_info:
            for actor in actors_info:
                actor_info = f"Имя: {actor['primaryName']}, Год рождения: {actor['birthYear']}, Год смерти: {actor['deathYear']}\nЗанятие: {actor['primaryProfession']}\n"
                bot.send_message(message.chat.id, actor_info)
        else:
            bot.send_message(message.chat.id, f"Нет данных об актерах в заданном диапазоне годов.")
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный формат года. Пожалуйста, введите корректный год (гггг).')
