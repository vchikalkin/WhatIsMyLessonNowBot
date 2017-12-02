import datetime

import pytz

# STARTUP PARAMETERS
weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
weekends = ["Воскресенье"]
week = "Числитель"
timezone = pytz.timezone('Europe/Moscow')

admin_id = 116570554
week_file = "week.txt"


# STARTUP PARAMETERS

def get_week():
    return week


def set_week(w):
    global week
    week = w
    save_week(w)


def get_day():
    today = datetime.datetime.today().weekday()
    return weekdays[today]


def get_current_date_and_time():
    return datetime.datetime.now(timezone).strftime("%d.%m.%Y %H:%M:%S")


def get_current_time():
    return datetime.datetime.now(timezone).strftime("%H:%M")


def save_week(w):
    with open(week_file, 'w') as text_file:
        text_file.write(w)
        text_file.truncate()
        text_file.close()


# USER'S CHAT TEMP VARIABLES
user_week = week
user_day = get_day()
user_university = ""
user_group = ""
# USER'S CHAT TEMP VARIABLES
