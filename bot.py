import telebot

import database
import settings

bot = telebot.TeleBot("419654586:AAGl98vEWE0iY9xXhnnwHygJ6bq7jwakQDY")


def log(message, answer):
    print("\n-----------------------------")
    from datetime import datetime
    print("[{0}]".format(datetime.now()))
    print("User - {0} {1}. (id = {2}) \n\nMessage - {3} \n\nAnswer - {4}".format(message.from_user.first_name,
                                                                                 message.from_user.last_name,
                                                                                 str(message.from_user.id),
                                                                                 message.text,
                                                                                 answer))


@bot.message_handler(commands=['about'])
def handle_text(message):
    bot.send_message(message.chat.id,
                     "Schedule Bot by Chika.\nNow only for 647M RSREU group\nhttps://vk.com/chikalkin")
    send_days_keyboard(message)


def send_days_keyboard(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Понедельник', 'Вторник')
    user_markup.row('Среда', 'Четверг')
    user_markup.row('Пятница')
    user_markup.row('КУДА МНЕ ИДТИ?')
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


@bot.message_handler(commands=["start"])
def handle_text(message):
    send_days_keyboard(message)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == "Понедельник" or message.text == "Вторник" or message.text == "Среда" or message.text == 'Четверг' or message.text == 'Пятница':
        settings.day = message.text
        send_week_keyboard(message)

    elif message.text == "Числитель" or message.text == "Знаменатель":
        settings.week = message.text
        bot.send_chat_action(message.chat.id, 'typing')
        answer = "*Пара* #1\n" + database.print_lesson(database.get_lesson(settings.day, settings.week, "1"))
        bot.send_message(message.chat.id, answer, parse_mode="Markdown")
        bot.send_chat_action(message.chat.id, 'typing')
        answer = "*Пара* #2\n" + database.print_lesson(database.get_lesson(settings.day, settings.week, "2"))
        bot.send_message(message.chat.id, answer, parse_mode="Markdown")
        send_days_keyboard(message)

    elif message.text == "Выбрать день":
        send_days_keyboard(message)

    elif message.text == "КУДА МНЕ ИДТИ?":
        bot.send_chat_action(message.chat.id, 'typing')
        hour = settings.get_hour()
        day = settings.get_day()
        if day != "Суббота" and day != "Воскресенье":
            if 0 <= hour < 15:
                answer = "Похоже, пары не скоро."
            elif 15 <= hour < 18:
                temp = database.print_lesson_force(database.get_lesson_force("1"))
                if not temp:
                    answer = "Похоже, первой пары нет."
                else:
                    answer = temp
            elif 18 <= hour < 19:
                temp = database.print_lesson_force(database.get_lesson_force("2"))
                if not temp:
                    answer = "Похоже, второй пары нет."
                else:
                    answer = temp
            elif 19 <= hour <= 23:
                answer = "Ты уже никуда не успеешь."
        else:
            answer = "Сегодня выходной! Отдыхай."
        bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
