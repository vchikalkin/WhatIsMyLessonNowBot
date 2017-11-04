import datetime

import telebot

import database
import settings

bot = telebot.TeleBot("419654586:AAGl98vEWE0iY9xXhnnwHygJ6bq7jwakQDY")

# ADMIN PARAMETERS
admin_id = 116570554


def send_admin_keyboard():
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/setup', '/setdown')
    user_markup.row('Выбрать день')
    answer = "Установлен параметр '" + settings.get_week() + "'\n /setup - чтобы изменить на *Числитель* \n /setdown - чтобы изменить на *Знаменатель*"
    bot.send_message(admin_id, answer, parse_mode="Markdown", reply_markup=user_markup)


message = "[[{0}]] Бот запущен".format(settings.get_current_date_and_time())
bot.send_message(admin_id, message, parse_mode="Markdown")
send_admin_keyboard()


# ADMIN PARAMETERS

def log(message, answer):
    print("\n-----------------------------")
    print("[{0}]".format(datetime.now()))
    print("User - {0} {1}. (id = {2}) \n\nMessage - {3} \n\nAnswer - {4}".format(message.from_user.first_name,
                                                                                 message.from_user.last_name,
                                                                                 str(message.from_user.id),
                                                                                 message.text,
                                                                                 answer))


def send_days_keyboard(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    if message.from_user.id != admin_id:
        user_markup.row('Понедельник', 'Вторник')
        user_markup.row('Среда', 'Четверг')
        user_markup.row('Пятница')
        user_markup.row('КУДА МНЕ ИДТИ?')
    else:
        user_markup.row('Понедельник', 'Вторник')
        user_markup.row('Среда', 'Четверг')
        user_markup.row('Пятница')
        user_markup.row('КУДА МНЕ ИДТИ?')
        user_markup.row('/admin')
    answer = "Выбери день...\n_(Сегодня {0}, если что)_".format(settings.get_day())
    bot.send_message(message.from_user.id, answer, parse_mode="Markdown", reply_markup=user_markup)


def send_week_keyboard(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Числитель', 'Знаменатель')
    user_markup.row('Выбрать день')
    answer = "Выбери неделю...\n_(Сейчас {0}, если что)_".format(settings.get_week())
    bot.send_message(message.from_user.id, answer, parse_mode="Markdown", reply_markup=user_markup)


def send_hide_keyboard(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "...", reply_markup=hide_markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    # ADMIN SETTINGS
    if message.from_user.id == admin_id and message.text == "/admin":
        send_admin_keyboard()
    elif message.from_user.id == admin_id and message.text == "/setup":
        settings.week = "Числитель"
        answer = "Установлен параметр '" + settings.get_week() + "'"
        print(answer)
        bot.send_message(message.chat.id, answer)
        send_days_keyboard(message)
    elif message.from_user.id == admin_id and message.text == "/setdown":
        settings.week = "Знаменатель"
        answer = "Установлен параметр '" + settings.get_week() + "'"
        print(answer)
        bot.send_message(message.chat.id, answer)
        send_days_keyboard(message)
    # ADMIN SETTINGS

    # MAIN
    if message.text in settings.weekdays:  # DETECT INPUT USER_DAY
        settings.user_day = message.text
        send_week_keyboard(message)

    elif message.text == "Числитель" or message.text == "Знаменатель":
        settings.user_week = message.text
        num = database.count_lessons(settings.user_day, settings.user_week)
        if not num:
            answer = "Похоже, в этот день пар нет."
            bot.send_message(message.chat.id, answer, parse_mode="Markdown")
        else:
            for i in range(len(num)):
                bot.send_chat_action(message.chat.id, 'typing')
                answer = database.get_lesson(settings.user_day, settings.user_week, num[i][0])
                bot.send_message(message.chat.id, answer, parse_mode="Markdown")
        send_days_keyboard(message)

    elif message.text == "Выбрать день":
        send_days_keyboard(message)
    # MAIN

    # FORCE GET LESSON
    elif message.text == "КУДА МНЕ ИДТИ?":
        bot.send_chat_action(message.chat.id, 'typing')
        day = settings.get_day()
        if day in settings.weekends:  # DETECT WEEKEND
            answer = "Сегодня выходной! Отдыхай."
        else:
            week = settings.get_week()
            time_frames = database.find_time_frames(day, week, 1)
            if not time_frames:
                answer = "Похоже, сегодня нет пар."
            else:
                time_start = time_frames[0]
                # time_end = time_frames[1]
                time_end = "23:59"
                current_time = settings.get_current_time()
                if time_start <= str(current_time) <= time_end:
                    answer = database.get_lesson_force(day, week, current_time)
                else:
                    answer = "Похоже, пары не скоро."
        bot.send_message(message.chat.id, answer, parse_mode="Markdown")
        # FORCE GET LESSON


@bot.message_handler(commands=["start"])
def handle_text(message):
    send_days_keyboard(message)


@bot.message_handler(commands=['about'])
def handle_text(message):
    answer = "Schedule Bot by Chika.\nNow only for 647M RSREU group\nhttps://vk.com/chikalkin"
    bot.send_message(message.chat.id, answer)
    send_days_keyboard(message)


bot.polling(none_stop=True)
