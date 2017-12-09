import datetime

import pytz

# PARAMETERS

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
weekends = ["Воскресенье"]

week_file_path = "week.txt"
token_file_path = "token.txt"
# TODO automatic week counter
week = "Числитель"

timezone = pytz.timezone('Europe/Moscow')

admin_id = 116570554

delta_hour = 1
delta_minute = 30


# PARAMETERS

def get_week():
    return week


def set_week(w):
    global week
    week = w
    save_week(w)
    system_message = "Applied parameter *'" + week + "'*"
    from system import alert
    alert(system_message)
    from main import send_to_admin
    send_to_admin(system_message)


def get_current_day():
    today = datetime.datetime.today().weekday()
    return days[today]


def get_current_date_and_time():
    return datetime.datetime.now(timezone).strftime("%d.%m.%Y %H:%M:%S")


def get_current_date():
    return datetime.datetime.now(timezone).strftime("%d/%m")


def get_current_time():
    return datetime.datetime.now(timezone).strftime("%H:%M")


def save_week(w):
    with open(week_file_path, 'w') as text_file:
        text_file.write(w)
        text_file.truncate()
        text_file.close()
