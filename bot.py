import telebot

import settings
import sheets

import datetime

bot = telebot.TeleBot ("419654586:AAGl98vEWE0iY9xXhnnwHygJ6bq7jwakQDY")

now_week = sheets.now_week


def log(message, answer):
    print ("\n-----------------------------")
    from datetime import datetime
    print ("[{0}]".format (datetime.now ()))
    print ("User - {0} {1}. (id = {2}) \n\nMessage - {3} \n\nAnswer - {4}".format (message.from_user.first_name,
                                                                                   message.from_user.last_name,
                                                                                   str (message.from_user.id),
                                                                                   message.text,
                                                                                   answer))


@bot.message_handler (commands=['about'])
def handle_text(message):
    bot.send_message (message.chat.id,
                      "Schedule Bot by Chika.\nNow only for 647M RSREU group\nhttps://vk.com/chikalkin")
    send_days_keyboard (message)


def send_days_keyboard(message):
    user_markup = telebot.types.ReplyKeyboardMarkup (True, False)
    user_markup.row ('Понедельник', 'Вторник')
    user_markup.row ('Среда', 'Четверг')
    user_markup.row ('Пятница')
    user_markup.row ('Куда мне, блин, идти?')
    answer = "Выбери день...\n_(Сегодня {0}, если что)_".format (sheets.today)
    bot.send_message (message.from_user.id, answer, parse_mode="Markdown", reply_markup=user_markup)


def send_week_keyboard(message):
    user_markup = telebot.types.ReplyKeyboardMarkup (True, False)
    user_markup.row ('Числитель', 'Знаменатель')
    answer = "Выбери неделю...\n_(Сейчас {0}, если что)_".format (now_week)
    bot.send_message (message.from_user.id, answer, parse_mode="Markdown", reply_markup=user_markup)


def send_hide_keyboard(message):
    hide_markup = telebot.types.ReplyKeyboardRemove ()
    bot.send_message (message.from_user.id, "...", reply_markup=hide_markup)


@bot.message_handler (commands=["start"])
def handle_text(message):
    send_days_keyboard (message)


@bot.message_handler (content_types=["text"])
def handle_text(message):
    if message.text == "Пятница" or message.text == "Суббота":
        # bot.send_chat_action (message.chat.id, 'typing')
        answer = "В этот день нет пар. Отдыхай :)"
        bot.send_message (message.chat.id, answer)
        send_days_keyboard (message)

    elif message.text == "Воскресенье":
        answer = "Ты понимаешь, что ты поехавший? В воскресенье не бывает пар."
        bot.send_message (message.chat.id, answer, parse_mode="Markdown")
        send_days_keyboard (message)

    elif message.text == "Понедельник" or message.text == "Вторник" or message.text == "Среда" or message.text == 'Четверг':
        settings.day = message.text
        send_week_keyboard (message)

    elif message.text == "Числитель" or message.text == "Знаменатель":
        settings.week = message.text
        bot.send_chat_action (message.chat.id, 'typing')
        answer = "*Пара* #1\n" + sheets.get_first_lesson (settings.day, settings.week)
        bot.send_message (message.chat.id, answer, parse_mode="Markdown")
        bot.send_chat_action (message.chat.id, 'typing')
        answer = "*Пара* #2\n" + sheets.get_second_lesson (settings.day, settings.week)
        bot.send_message (message.chat.id, answer, parse_mode="Markdown")
        send_days_keyboard (message)

    elif message.text == "Куда мне, блин, идти?":
        bot.send_chat_action (message.chat.id, 'typing')
        hour = datetime.datetime.today ().hour
        # minute = datetime.datetime.today ().minute
        if 0 <= hour <= 12:
            answer = "Куда ты, блин, так рано собрался?"
        elif 12 <= hour < 18:
            answer = (sheets.get_aud_force ("1"))
        elif 18 <= hour < 19:
            answer = (sheets.get_aud_force ("2"))
        elif hour >= 19:
            answer = "Ты, блин, уже никуда не успеешь."
        bot.send_message (message.chat.id, answer)


bot.polling (none_stop=True, interval=0)
