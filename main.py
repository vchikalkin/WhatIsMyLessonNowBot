import telebot

import keyboards
import schedule
import settings
import system
import users

bot = telebot.TeleBot()


def send_keyboard(id, answer, markup):
    bot.send_message(id, answer, parse_mode="Markdown", reply_markup=markup)


def send_to_admin(message):
    bot.send_message(settings.admin_id, message, parse_mode="Markdown")


def handle_text(user_id, message, day, week):
    # ADMIN SETTINGS
    if user_id == settings.admin_id:
        if message.text == "/Числитель" or message.text == "/Знаменатель":
            if message.text == "/Числитель":
                settings.set_week("Числитель")
            elif message.text == "/Знаменатель":
                settings.set_week("Знаменатель")
            answer = "Установлен параметр '" + settings.get_week() + "'"
            system.alert(answer)
            send_to_admin(answer)
            send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)
        elif message.text == "Выбрать неделю":
            send_keyboard(user_id, keyboards.AdminKeyboard.answer, keyboards.AdminKeyboard.markup)
    # ADMIN SETTINGS

    # AUTHENTICATION
    if not users.exist(user_id):
        if message.text in users.get_universities():
            settings.user_university = message.text
            send_keyboard(user_id, keyboards.GroupsKeyboard.answer, keyboards.GroupsKeyboard.markup)
        elif message.text in users.get_groups(settings.user_university):
            university = settings.user_university
            group = message.text
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            users.register(user_id, university, group, first_name, last_name)
            day = settings.get_day()
            send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)
        else:
            send_keyboard(user_id, keyboards.UniversitiesKeyboard.answer, keyboards.UniversitiesKeyboard.markup)
        # AUTHENTICATION

    else:
        user_where_from = users.where_from(user_id)
        settings.user_university = user_where_from[0]
        settings.user_group = user_where_from[1]

        # SETTINGS
        if message.text == "Настройки":
            send_keyboard(user_id, keyboards.SettingsKeyboard.answer, keyboards.SettingsKeyboard.get_markup(user_id))
        if message.text == "Сменить группу":
            answer = "Сейчас ты зарегистрирован в группе *{0}*".format(settings.user_group)
            bot.send_message(user_id, answer, parse_mode="Markdown")
            send_keyboard(user_id, keyboards.GroupsKeyboard.answer, keyboards.GroupsKeyboard.markup)
        if message.text in users.get_groups(settings.user_university):
            university = settings.user_university
            group = message.text
            users.move_user(user_id, group)
            send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)
        # SETTINGS

        # MAIN
        if message.text in settings.weekdays:  # DETECT INPUT USER_DAY
            settings.user_day = message.text
            send_keyboard(user_id, keyboards.WeekKeyboard.get_week(week), keyboards.WeekKeyboard.markup)

        elif message.text == "Числитель" or message.text == "Знаменатель":
            settings.user_week = message.text
            num = schedule.count_lessons(settings.user_university, settings.user_group, settings.user_day,
                                         settings.user_week)
            if not num:
                answer = "Похоже, в этот день пар нет."
                bot.send_message(user_id, answer, parse_mode="Markdown")
            else:
                for i in range(len(num)):
                    bot.send_chat_action(user_id, 'typing')
                    answer = schedule.get_lesson(settings.user_university, settings.user_group, settings.user_day,
                                                 settings.user_week, num[i][0])
                    bot.send_message(user_id, answer, parse_mode="Markdown")
            send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)

        elif message.text == "Выбрать день" or message.text == "Назад":
            send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)
        # MAIN

        # FORCE GET LESSON
        elif message.text == "КУДА МНЕ ИДТИ?":
            bot.send_chat_action(user_id, 'typing')
            if day in settings.weekends:  # DETECT WEEKEND
                answer = "Сегодня выходной!"
            else:
                time_frames = schedule.find_time_frames(settings.user_university, settings.user_group, day, week, 1, 30)
                if not time_frames:
                    answer = "Похоже, сегодня нет пар."
                else:
                    time_start = time_frames[0]
                    # time_end = time_frames[1]
                    time_end = "23:59"
                    current_time = settings.get_current_time()
                    if time_start <= str(current_time) <= time_end:
                        answer = schedule.get_lesson_force(settings.user_university, settings.user_group, day, week,
                                                           current_time)
                    else:
                        answer = "Похоже, пары не скоро."
            bot.send_message(user_id, answer, parse_mode="Markdown")
            # FORCE GET LESSON

        # NOTIFIER
        # TODO
        # NOTIFIER
