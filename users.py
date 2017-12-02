import sqlite3

connection = sqlite3.connect('users.db', check_same_thread=False)


def get_universities():
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT UNIVERSITY FROM groups")
    result = cursor.fetchall()
    cursor.close()
    return result[0]


def get_groups(university):
    cursor = connection.cursor()
    cursor.execute("SELECT GROUP_NAME FROM groups WHERE UNIVERSITY = (?)", (university,))
    result = cursor.fetchall()
    result2 = []
    for i in result:
        result2.append(i[0])
    cursor.close()
    return result2


def exist(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE TG_ID = (?)", (id,))
    result = cursor.fetchall()
    cursor.close()
    return result


def where_from(id):
    if exist(id):
        cursor = connection.cursor()
        cursor.execute("SELECT ST_UNIVERSITY, ST_GROUP FROM users WHERE TG_ID = (?)", (id,))
        result = cursor.fetchall()
        cursor.close()
        return result[0]


def register(id, university, group, first_name, last_name):
    if not exist(id):
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (TG_ID, ST_UNIVERSITY, ST_GROUP, FIRST_NAME, LAST_NAME) VALUES ((?), (?), (?), (?), (?))",
            (id, university, group, first_name, last_name))
        connection.commit()
        message = "User {0} successfully registered.".format(id)
        cursor.close()
    else:
        message = "User {0} already registered.".format(id)
    print("System Message: " + message)


def delete_user(id):
    if not exist(id):
        message = "User isn't registered"
    else:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE TG_ID=(?)", (id,))
        connection.commit()
        cursor.close()
        message = "User {0} is successfully deleted.".format(id)
    print("System Message: " + message)


def move_user(id, group):
    if not exist(id):
        message = "User isn't registered"
    else:
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET ST_GROUP = (?) WHERE TG_ID=(?)", (group, id))
        connection.commit()
        cursor.close()
        message = "User {0} moved to group {1}.".format(id, group)
    print("System Message: " + message)


def print_all():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    result = cursor.fetchall()
    cursor.close()
    print(result)
