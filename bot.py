import os

import keyboards
import main
import settings
import system
from main import bot

# STARTUP PARAMETERS
system_message = "[[{0}]] Бот запущен".format(settings.get_current_date_and_time())

if os.path.isfile(settings.week_file) and os.path.getsize(settings.week_file) > 0:
    # system_message += "\nФайл " + settings.week_file + " найден"
    with open(settings.week_file) as text_file:
        content = text_file.readline()
        settings.week = content
system_message += "\nУстановлен параметр *'" + settings.get_week() + "'*"
system.alert(system_message)
main.send_to_admin(system_message)


# STARTUP PARAMETERS


@bot.message_handler(content_types=["text"])
def handle_text(message):
    system.log(message)
    user_id = message.from_user.id
    day = settings.get_day()
    week = settings.get_week()
    main.handle_text(user_id, message, day, week)


@bot.message_handler(commands=["start"])
def handle_text(message):
    user_id = message.from_user.id
    day = settings.get_day()
    main.send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)


@bot.message_handler(commands=["settings"])
def handle_text(message):
    user_id = message.from_user.id
    main.send_keyboard(user_id, keyboards.SettingsKeyboard.answer, keyboards.SettingsKeyboard.get_markup(user_id))


@bot.message_handler(commands=['about'])
def handle_text(message):
    user_id = message.from_user.id
    day = settings.get_day()
    answer = "Schedule Bot by Chika.\nNow only for 647M RSREU group\nhttps://vk.com/chikalkin"
    bot.send_message(user_id, answer)
    main.send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)


bot.polling(none_stop=True)
