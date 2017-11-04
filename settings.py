import datetime

import pytz

# RUN PARAMETERS
weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
weekends = ["Суббота", "Воскресенье"]
timezone = pytz.timezone('Europe/Moscow')
week = "Числитель"


# RUN PARAMETERS

def get_week():
    return week


def get_day():
    today = datetime.datetime.today().weekday()
    return weekdays[today]


def get_current_date_and_time():
    return datetime.datetime.now(timezone).strftime("%d.%m.%Y %H:%M:%S")


def get_current_time():
    return datetime.datetime.now(timezone).strftime("%H:%M")


# USER'S CHAT VARIABLES
user_week = week
user_day = get_day()
# USER'S CHAT VARIABLES
