import sqlite3

import settings

connection = sqlite3.connect('schedule.db', check_same_thread=False)


def get_lesson_force(num):
    cursor = connection.cursor()
    day = settings.get_day()
    week = settings.get_week()
    cursor.execute("SELECT AUDIENCE, FIO FROM m647 WHERE DAY = (?) AND WEEK=(?) AND NUM = (?)", (day, week, num))
    result = cursor.fetchall()
    cursor.close()
    return result


def print_lesson_force(input):
    l = list(input)
    if not l:
        return l
    return "Тебе в " + str(l[0][0]) + ". Там тебя ждет " + str(l[0][1])


def get_lesson(day, week, num):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT TIME_START, TIME_END, AUDIENCE, TYPE, NAME, FIO FROM m647 WHERE DAY = (?) AND WEEK=(?) AND NUM = (?)",
        (day, week, num))
    result = cursor.fetchall()
    cursor.close()
    return result


def print_lesson(input):
    l = list(input)
    if not l:
        return "Похоже, этой пары нет."
    return "Время: " + str(l[0][0]) + "-" + str(l[0][1]) + "\n" \
                                                           "Ауд.: " + str(l[0][2]) + "\n" + \
           "Тип: " + str(l[0][3]) + "\n" + \
           "Назв.: " + str(l[0][4]) + "\n" + \
           "Препод: " + str(l[0][5])
