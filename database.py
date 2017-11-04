import sqlite3
import datetime
from datetime import timedelta

connection = sqlite3.connect('schedule.db', check_same_thread=False)


# MAIN
def count_lessons(day, week):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT NUM FROM m647 WHERE DAY = (?) AND WEEK=(?)",
        (day, week))
    result = cursor.fetchall()
    cursor.close()
    return result


def find_lesson(day, week, num):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT TIME_START, TIME_END, AUDIENCE, TYPE, NAME, FIO FROM m647 WHERE DAY = (?) AND WEEK = (?) AND NUM = (?)",
        (day, week, num))
    result = cursor.fetchall()
    cursor.close()
    return result


def get_lesson(day, week, num):
    lesson = list(find_lesson(day, week, num))
    if not lesson:
        return "Похоже, этой пары нет."
    return "*Пара #{0}*".format(num) + "\n" + \
           "Время: " + str(lesson[0][0]) + "-" + str(lesson[0][1]) + "\n" + \
           "Ауд.: " + str(lesson[0][2]) + "\n" + \
           "Тип: " + str(lesson[0][3]) + "\n" + \
           "Назв.: " + str(lesson[0][4]) + "\n" + \
           "Препод: " + str(lesson[0][5])


# MAIN


# FORCE GET LESSON
def find_time_frames(day, week, delta):
    cursor = connection.cursor()
    cursor.execute("SELECT MIN(TIME_START), MAX(TIME_END) FROM m647 WHERE DAY = (?) AND WEEK = (?)", (day, week))
    result = cursor.fetchall()
    result = list(result)
    if not result[0][0]:
        return None
    else:
        time_start = (datetime.datetime.strptime(result[0][0], '%H:%M') - timedelta(hours=delta)).strftime('%H:%M')
        time_end = result[0][1]
        result = [time_start, time_end]
    cursor.close()
    return result


def find_current_lesson(day, week, time):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT AUDIENCE, TIME_END, FIO FROM m647 WHERE DAY = (?) AND WEEK = (?) AND TIME_START <= (?) AND TIME_END >= (?)",
        (day, week, time, time))
    result = cursor.fetchall()
    cursor.close()
    if not result:
        return None
    return result[0]


def find_next_lesson(day, week, time):
    cursor = connection.cursor()
    cursor.execute("SELECT TIME_START, AUDIENCE, FIO FROM m647 WHERE DAY = (?) AND WEEK = (?) AND TIME_START > (?)",
                   (day, week, time))
    result = cursor.fetchall()
    cursor.close()
    if not result:
        return None
    return result[0]


def get_lesson_force(day, week, time):
    current_lesson = find_current_lesson(day, week, time)
    next_lesson = find_next_lesson(day, week, time)
    answer = ""
    if current_lesson:
        answer = "Сейчас идет пара в ауд. *№{0}* \nОна закончится в *{1}*\nПрепод: {2}\n".format(current_lesson[0],
                                                                                                 current_lesson[1],
                                                                                                 current_lesson[2])
        if next_lesson:
            answer += "\nСледующая пара начнется в *{0}* \nАуд. *№{1}* \nПрепод: {2}".format(next_lesson[0],
                                                                                             next_lesson[1],
                                                                                             next_lesson[2])
        elif not next_lesson:
            answer += "\nЭто последняя пара :)"

    elif not current_lesson:
        if next_lesson:
            answer = "Ближайшая пара начнется в *{0}* \nАуд. *№{1}* \nПрепод: {2}".format(next_lesson[0],
                                                                                          next_lesson[1],
                                                                                          next_lesson[2])
        elif not next_lesson:
            answer = "Все пары сегодня закончились :)"
    return answer

# FORCE GET LESSON
