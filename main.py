import telebot

import keyboards
import schedule
import settings
import user
import users

bot = telebot.TeleBot("token")

user = user.User()


def send_keyboard(id, answer, markup):
    bot.send_message(id, answer, parse_mode="Markdown", reply_markup=markup)


def send_to_admin(message):
    bot.send_message(settings.admin_id, "*{0}*".format(message), parse_mode="Markdown")


def handle_text_admin(user_id, message, day):
    if message.text == "/Числитель" or message.text == "/Знаменатель":
        if message.text == "/Числитель":
            settings.set_week("Числитель")
        elif message.text == "/Знаменатель":
            settings.set_week("Знаменатель")
        send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)
    elif message.text == "Выбрать неделю":
        send_keyboard(user_id, keyboards.AdminKeyboard.answer, keyboards.AdminKeyboard.markup)


def handle_text_settings(user_id, message):
    if message.text == "Настройки":
        send_keyboard(user_id, keyboards.SettingsKeyboard.answer, keyboards.SettingsKeyboard.get_markup(user_id))
    if message.text == "Сменить группу":
        answer = "Ты был зарегистрирован в группе *{0}*".format(user.group)
        bot.send_message(user_id, answer, parse_mode="Markdown")
        users.delete_user(user_id)
        send_keyboard(user_id, keyboards.UniversitiesKeyboard.answer, keyboards.UniversitiesKeyboard.markup)


def handle_text_force(user_id, day, week):
    bot.send_chat_action(user_id, 'typing')
    if day in settings.weekends:  # DETECT WEEKEND
        answer = "Сегодня выходной!"
    else:
        time_frames = schedule.find_time_frames(user.university, user.group, day, week,
                                                settings.delta_hour, settings.delta_minute)
        if not time_frames:
            answer = "Похоже, сегодня нет пар."
        else:
            time_start = time_frames[0]
            # time_end = time_frames[1]
            time_end = "23:59"
            current_time = settings.get_current_time()
            if time_start <= str(current_time) <= time_end:
                answer = schedule.get_lesson_force(user.university, user.group, day, week,
                                                   current_time)
            else:
                answer = "Похоже, пары не скоро."
    bot.send_message(user_id, answer, parse_mode="Markdown")


def handle_text_main(user_id, message, day, week):
    user_where_from = users.where_from(user_id)
    user.university = user_where_from[0]
    user.group = user_where_from[1]

    # MAIN
    if message.text in settings.weekdays:  # DETECT INPUT USER_DAY
        user.day = message.text
        send_keyboard(user_id, keyboards.WeekKeyboard.get_week(week), keyboards.WeekKeyboard.markup)
    elif message.text == "Числитель" or message.text == "Знаменатель":
        user.week = message.text
        num = schedule.count_lessons(user.university, user.group, user.day,
                                     user.week)
        if not num:
            answer = "Похоже, в этот день пар нет."
            bot.send_message(user_id, answer, parse_mode="Markdown")
        else:
            for i in range(len(num)):
                bot.send_chat_action(user_id, 'typing')
                answer = schedule.get_lesson(user.university, user.group, user.day,
                                             user.week, num[i][0])
                bot.send_message(user_id, answer, parse_mode="Markdown")
        send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)
    elif message.text == "Выбрать день" or message.text == "Назад":
        send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)
    # MAIN

    # FORCE GET LESSON
    elif message.text == "КУДА МНЕ ИДТИ?":
        handle_text_force(user_id, day, week)
    # FORCE GET LESSON

    # SETTINGS
    if message.text == "Настройки" or message.text == "Сменить группу":
        handle_text_settings(user_id, message)
    # SETTINGS

# NOTIFIER
# TODO
# NOTIFIER
