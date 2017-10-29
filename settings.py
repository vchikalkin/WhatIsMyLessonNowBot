import datetime

import pytz


def get_day():
    dayofweek = datetime.datetime.today().weekday()
    day_list = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return day_list[dayofweek]


def get_week():
    return "Знаменатель"
    # return sheets.sheet.cell (23, 2).value


def get_hour():
    timezone = pytz.timezone('Europe/Moscow')
    return datetime.datetime.now(timezone).hour


day = get_day()
week = get_week()
