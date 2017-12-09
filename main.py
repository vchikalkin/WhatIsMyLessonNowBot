import telebot

import groups
import keyboards
import schedule
import settings
import user
import users

token_file = settings.token_file_path
from system import read_file

token = read_file(token_file)

bot = telebot.TeleBot(token)

current_user = user.User()


def send_keyboard(id, answer, markup):
    bot.send_message(id,
                     answer,
                     parse_mode="Markdown",
                     reply_markup=markup)


def send_to_admin(message):
    bot.send_message(settings.admin_id,
                     "*{0}*".format(message),
                     parse_mode="Markdown")


def handle_text_admin(user_id, message, day):
    if message.text == "/Числитель" or message.text == "/Знаменатель":
        if message.text == "/Числитель":
            settings.set_week("Числитель")
        elif message.text == "/Знаменатель":
            settings.set_week("Знаменатель")
        send_keyboard(user_id,
                      keyboards.DaysKeyboard.get_answer(day),
                      keyboards.DaysKeyboard.markup)
    elif message.text == "Выбрать неделю":
        send_keyboard(user_id,
                      keyboards.AdminKeyboard.answer,
                      keyboards.AdminKeyboard.markup)


def handle_text_settings(user_id, message):
    if message.text == "Настройки":
        send_keyboard(user_id,
                      keyboards.SettingsKeyboard.answer,
                      keyboards.SettingsKeyboard.get_markup(user_id))
    if message.text == "Сменить группу":
        users_group = groups.get_group_rus(current_user.group)
        users_university = groups.get_university_rus(current_user.university)
        answer = "Ты был зарегистрирован в группе *{0}, {1}*".format(users_group,
                                                                     users_university)
        bot.send_message(user_id,
                         answer,
                         parse_mode="Markdown")
        users.delete_user(user_id)
        send_keyboard(user_id,
                      keyboards.UniversitiesKeyboard.answer,
                      keyboards.UniversitiesKeyboard.markup)


def handle_text_force(user_id, day, week):
    bot.send_chat_action(user_id, 'typing')
    if day not in settings.weekends:  # DETECT WEEKEND
        lesson_ids = schedule.find_lesson_id(current_user.university,
                                             current_user.group,
                                             day,
                                             week)

        time_frames = schedule.find_time_frames(current_user.university,
                                                current_user.group,
                                                day,
                                                week)
        if lesson_ids and time_frames[0]:
            import datetime
            time_start = (datetime.datetime.strptime(time_frames[0], '%H:%M')
                          - datetime.timedelta(hours=settings.delta_hour,
                                               minutes=settings.delta_minute)).strftime('%H:%M')
            time_end = "23:59"
            current_time = settings.get_current_time()
            if time_start <= str(current_time) <= time_end:
                answer = schedule.get_lesson_force(current_user.university,
                                                   current_user.group,
                                                   day,
                                                   week,
                                                   current_time)
            else:
                answer = "Похоже, пары не скоро."
        else:
            answer = "Похоже, сегодня нет пар."
    else:
        answer = "Сегодня выходной!"

    bot.send_message(user_id, answer, parse_mode="Markdown")


def handle_text_main(user_id, message, day, week):
    user_where_from = users.where_from(user_id)
    current_user.university = user_where_from[0]
    current_user.group = user_where_from[1]

    # MAIN
    if message.text in settings.days:  # DETECT INPUT USER_DAY
        current_user.day = message.text
        send_keyboard(user_id,
                      keyboards.WeekKeyboard.get_week(week),
                      keyboards.WeekKeyboard.markup)

    elif message.text == "Числитель" or message.text == "Знаменатель":
        current_user.week = message.text
        lesson_id = schedule.find_lesson_id(current_user.university,
                                            current_user.group,
                                            current_user.day,
                                            current_user.week)

        if not lesson_id:
            answer = "Похоже, в этот день пар нет."
            bot.send_message(user_id,
                             answer,
                             parse_mode="Markdown")

        else:
            for i in range(len(lesson_id)):
                bot.send_chat_action(user_id, 'typing')
                answer = schedule.get_lesson(current_user.university,
                                             current_user.group,
                                             current_user.day,
                                             current_user.week,
                                             lesson_id[i][0])
                bot.send_message(user_id,
                                 answer,
                                 parse_mode="Markdown")

        send_keyboard(user_id,
                      keyboards.DaysKeyboard.get_answer(day),
                      keyboards.DaysKeyboard.markup)

    elif message.text == "Выбрать день" or message.text == "Назад":
        send_keyboard(user_id,
                      keyboards.DaysKeyboard.get_answer(day),
                      keyboards.DaysKeyboard.markup)
    # MAIN

    # FORCE GET LESSON
    elif message.text == "КУДА МНЕ ИДТИ?":
        handle_text_force(user_id,
                          day,
                          week)
    # FORCE GET LESSON

    # SETTINGS
    if message.text == "Настройки" or message.text == "Сменить группу":
        handle_text_settings(user_id,
                             message)
    # SETTINGS

# NOTIFIER
# TODO
# NOTIFIER
