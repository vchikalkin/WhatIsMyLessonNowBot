import sqlite3

connection = sqlite3.connect('groups.db', check_same_thread=False)


def get_universities():
    cursor = connection.cursor()
    cursor.execute("SELECT "
                   "        RUS "
                   "FROM "
                   "        universities")
    result = cursor.fetchall()
    cursor.close()
    return result[0]


def get_university_eng(university):
    cursor = connection.cursor()
    cursor.execute("SELECT "
                   "        UNIVERSITY "
                   "FROM "
                   "        universities "
                   "WHERE "
                   "        RUS = (?)",
                   (university,))
    result = cursor.fetchall()
    cursor.close()
    return result[0][0]


def get_university_rus(university_eng):
    cursor = connection.cursor()
    cursor.execute("SELECT "
                   "        RUS "
                   "FROM "
                   "        universities "
                   "WHERE "
                   "        UNIVERSITY = (?)",
                   (university_eng,))
    result = cursor.fetchall()
    cursor.close()
    return result[0][0]


def get_groups(university):
    cursor = connection.cursor()
    cursor.execute("SELECT "
                   "        RUS "
                   "FROM "
                   "        groups "
                   "WHERE "
                   "        UNIVERSITY = (?)",
                   (university,))
    result = cursor.fetchall()
    temp = result
    result = []
    for i in temp:
        result.append(i[0])
    cursor.close()
    return result


def get_group_eng(group):
    cursor = connection.cursor()
    cursor.execute("SELECT "
                   "        GROUP_NAME "
                   "FROM "
                   "        groups "
                   "WHERE "
                   "        RUS = (?)",
                   (group,))
    result = cursor.fetchall()
    cursor.close()
    return result[0][0]


def get_group_rus(group_eng):
    cursor = connection.cursor()
    cursor.execute("SELECT "
                   "        RUS "
                   "FROM "
                   "        groups "
                   "WHERE "
                   "        GROUP_NAME = (?)",
                   (group_eng,))
    result = cursor.fetchall()
    cursor.close()
    return result[0][0]
