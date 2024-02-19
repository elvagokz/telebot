from ..site_API.api_request import get_actors

def handle_low(bot, message):
    # Запросить количество актеров у пользователя
    bot.send_message(message.chat.id, 'Введите количество актёров:')
    # Установить состояние пользователя, чтобы следующее сообщение обрабатывалось как ответ на этот вопрос
    bot.register_next_step_handler(message, lambda m: handle_low_response(bot, m))

def handle_low_response(bot, message):
    try:
        # Попытка преобразовать введенное количество актеров в число
        num_actors_to_display = int(message.text)

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
