import datetime

import pytz

timezone = pytz.timezone('Europe/Moscow')


def get_day():
    dayofweek = datetime.datetime.today().weekday()
    day_list = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return day_list[dayofweek]


day = get_day()


def get_hour():
    return datetime.datetime.now(timezone).hour


def get_current_time():
    return datetime.datetime.now(timezone).strftime("%d.%m.%Y %H:%M:%S")


def get_week():
    return week


week = "Числитель"
user_week = week
