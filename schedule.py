import datetime
import sqlite3
from datetime import timedelta

connection = sqlite3.connect('schedule.db', check_same_thread=False)


# MAIN
def count_lessons(university, group, day, week):
    cursor = connection.cursor()
    cursor.execute("SELECT NUM FROM {0} WHERE ST_GROUP = (?) AND DAY = (?) AND WEEK = (?)".format(university),
                   (group, day, week))
    result = cursor.fetchall()
    cursor.close()
    return result


def find_lesson(university, group, day, week, num):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT TIME_START, TIME_END, AUDIENCE, TYPE, NAME, FIO FROM {0} WHERE ST_GROUP = (?) AND DAY = (?) AND WEEK = (?) AND NUM = (?)".format(
            university),
        (group, day, week, num))
    result = cursor.fetchall()
    cursor.close()
    return result


def get_lesson(university, group, day, week, num):
    lesson = list(find_lesson(university, group, day, week, num))
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
def find_time_frames(university, group, day, week, hours_delta, minutes_delta):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT MIN(TIME_START), MAX(TIME_END) FROM {0} WHERE ST_GROUP = (?) AND DAY = (?) AND WEEK = (?)".format(
            university),
        (group, day, week))
    result = cursor.fetchall()
    result = list(result)
    if not result[0][0]:
        return None
    else:
        time_start = (datetime.datetime.strptime(result[0][0], '%H:%M') - timedelta(hours=hours_delta,
                                                                                    minutes=minutes_delta)).strftime(
            '%H:%M')
        time_end = result[0][1]
        result = [time_start, time_end]
    cursor.close()
    return result


def find_current_lesson(university, group, day, week, time):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT AUDIENCE, TIME_END, FIO FROM {0} WHERE ST_GROUP = (?) AND DAY = (?) AND WEEK = (?) AND TIME_START <= (?) AND TIME_END >= (?)".format(
            university),
        (group, day, week, time, time))
    result = cursor.fetchall()
    cursor.close()
    if not result:
        return None
    return result[0]


def find_next_lesson(university, group, day, week, time):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT TIME_START, AUDIENCE, FIO FROM {0} WHERE ST_GROUP = (?) AND DAY = (?) AND WEEK = (?) AND TIME_START > (?)".format(
            university),
        (group, day, week, time))
    result = cursor.fetchall()
    cursor.close()
    if not result:
        return None
    return result[0]


def get_next_lesson(university, group, day, week, time):
    next_lesson = find_next_lesson(university, group, day, week, time)
    if next_lesson:
        answer = "НБлижайшая пара начнется в *{0}* \nАуд. *№{1}* \nПрепод: {2}".format(next_lesson[0],
                                                                                       next_lesson[1],
                                                                                       next_lesson[2])
    return answer


def get_lesson_force(university, group, day, week, time):
    current_lesson = find_current_lesson(university, group, day, week, time)
    next_lesson = find_next_lesson(university, group, day, week, time)
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
            answer += "\nЭто последняя пара! :)"

    elif not current_lesson:
        if next_lesson:
            answer = "Ближайшая пара начнется в *{0}* \nАуд. *№{1}* \nПрепод: {2}".format(next_lesson[0],
                                                                                          next_lesson[1],
                                                                                          next_lesson[2])
        elif not next_lesson:
            answer = "Все пары сегодня закончились."
    return answer

# FORCE GET LESSON
