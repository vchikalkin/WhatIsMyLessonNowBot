import sqlite3

connection = sqlite3.connect('schedule.db', check_same_thread=False)


# MAIN
def find_lesson_id(university, group, day, week):
    cursor = connection.cursor()
    cursor.execute("SELECT "
                   "        ID "
                   "FROM "
                   "        {0} "
                   "WHERE "
                   "        ST_GROUP = (?) "
                   "AND     DAY = (?) "
                   "AND     WEEK = (?)"
                   .format(university), (group, day, week))
    result = cursor.fetchall()
    cursor.close()
    return result


def find_dates(university, lesson_id):
    cursor = connection.cursor()
    cursor.execute("SELECT "
                   "        DATE "
                   "FROM "
                   "        {0} "
                   "WHERE "
                   "        ID = (?)"
                   .format(university + "_dates"), (lesson_id,))
    result = cursor.fetchall()
    result = list(result)
    temp = []
    for i in range(len(result)):
        temp.append(result[i][0])
    result = temp
    cursor.close()
    return result


def find_lesson(university, group, day, week, lesson_id):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT "
        "       NUM, "
        "       TIME_START, "
        "       TIME_END, "
        "       AUDIENCE, "
        "       TYPE, "
        "       NAME, "
        "       FIO "
        "FROM "
        "       {0} "
        "WHERE "
        "       ST_GROUP = (?) "
        "AND    DAY = (?) "
        "AND    WEEK = (?) "
        "AND    ID = (?)"
            .format(university), (group, day, week, lesson_id))
    result = cursor.fetchall()
    cursor.close()
    return result


def get_lesson(university, group, day, week, lesson_id):
    lesson = list(find_lesson(university, group, day, week, lesson_id))
    dates = find_dates(university, lesson_id)
    dates_list = ', '.join(dates).replace('/', '.')
    answer = ""
    if not lesson:
        return "Похоже, этой пары нет."
    else:
        answer += "*Пара #{0}*".format(lesson[0][0]) + "\n"
        if dates:
            answer += "Даты: _{0}_\n".format(dates_list)
        answer += "Время: " + str(lesson[0][1]) + "-" + str(lesson[0][2]) + "\n" + \
                  "Ауд.: " + str(lesson[0][3]) + "\n" + \
                  "Тип: " + str(lesson[0][4]) + "\n" + \
                  "Назв.: " + str(lesson[0][5]) + "\n" + \
                  "Препод(ы): " + str(lesson[0][6]) + "\n"
    return answer


# MAIN


# FORCE GET LESSON

def find_ignore_ids(university, group):
    from settings import get_current_date
    current_date = get_current_date()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT "
                   "        ID "
                   "FROM "
                   "        {0} "
                   "WHERE   ST_GROUP = (?)"
                   .format(university + "_dates"), (group,))
    result = cursor.fetchall()
    ignore_ids = []
    if not result:
        result = "(-1)"
    elif len(result) >= 1:
        for i in range(len(result)):
            ignore_ids.append(result[i][0])
        cursor.execute("SELECT "
                       "        ID "
                       "FROM    {0} "
                       "WHERE   DATE IN (?)"
                       .format(university + "_dates"), (current_date,))
        not_ignore_id = cursor.fetchall()
        if not_ignore_id:
            not_ignore_id = not_ignore_id[0][0]
            if not_ignore_id in ignore_ids:
                ignore_ids.remove(not_ignore_id)
        if len(ignore_ids) == 1:
            result = "({0})".format(ignore_ids[0])
        else:
            result = tuple(ignore_ids)
    cursor.close()
    return result


def find_time_frames(university, group, day, week):
    ignore_ids = find_ignore_ids(university, group)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT "
        "       MIN(TIME_START), "
        "       MAX(TIME_END) "
        "FROM   {0} "
        "WHERE "
        "       ST_GROUP = (?) "
        "AND    DAY = (?) "
        "AND    WEEK = (?) "
        "AND    ID NOT IN {1}"
            .format(university, ignore_ids), (group, day, week))
    result = cursor.fetchall()
    result = list(result)
    cursor.close()
    return result[0]


def find_current_lesson(university, group, day, week, time, ignore_ids):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT "
        "       AUDIENCE, "
        "       TIME_END, "
        "       FIO "
        "FROM "
        "       {0} "
        "WHERE "
        "       ST_GROUP = (?) "
        "AND    DAY = (?) "
        "AND    WEEK = (?) "
        "AND    TIME_START <= (?) "
        "AND    TIME_END >= (?) "
        "AND    ID NOT IN {1}"
            .format(university, ignore_ids), (group, day, week, time, time))
    result = cursor.fetchall()
    cursor.close()
    if not result:
        return None
    return result[0]


def find_next_lesson(university, group, day, week, time, ignore_ids):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT "
        "       TIME_START, "
        "       AUDIENCE, "
        "       FIO "
        "FROM "
        "       {0} "
        "WHERE "
        "       ST_GROUP = (?) "
        "AND    DAY = (?) "
        "AND    WEEK = (?) "
        "AND    TIME_START > (?) "
        "AND    ID NOT IN {1}"
            .format(university, ignore_ids), (group, day, week, time))
    result = cursor.fetchall()
    cursor.close()
    if not result:
        return None
    return result[0]


def get_lesson_force(university, group, day, week, time):
    ignore_ids = find_ignore_ids(university, group)
    current_lesson = find_current_lesson(university, group, day, week, time, ignore_ids)
    next_lesson = find_next_lesson(university, group, day, week, time, ignore_ids)
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
            answer += "\nИ это последняя пара на сегодня!"

    elif not current_lesson:
        if next_lesson:
            answer = "Ближайшая пара начнется в *{0}* \nАуд. *№{1}* \nПрепод: {2}".format(next_lesson[0],
                                                                                          next_lesson[1],
                                                                                          next_lesson[2])
        elif not next_lesson:
            answer = "Все пары сегодня закончились."
    return answer

# FORCE GET LESSON
