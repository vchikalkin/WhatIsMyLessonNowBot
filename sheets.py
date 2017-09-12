import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name ('googleauth.json', scope)
client = gspread.authorize (creds)

sheet = client.open ("Sheet1").sheet1

dayofweek = datetime.datetime.today ().weekday ()
# dayofweek = 1
day_list = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
today = day_list[dayofweek]
# today = "Понедельник"
now_week = sheet.cell (23, 2).value


# nowweek = "Числитель"


def get_row(day, num, week):
    days = sheet.findall (day)
    for d in days:
        row = d.row
        if sheet.cell (row, 2).value == week:
            if sheet.cell (row, 3).value == num:
                return row


def print_lesson(row):
    return "*Время:* " + sheet.cell (row, 4).value + "\n" \
                                                     "*Ауд.:* " + sheet.cell (row, 5).value + "\n" + \
           "*Тип:* " + sheet.cell (row, 6).value + "\n" + \
           "*Назв.:* " + sheet.cell (row, 7).value + "\n" + \
           "*Препод:* " + sheet.cell (row, 8).value


def get_first_lesson(day, week):
    row = get_row (day, "1", week)
    return print_lesson (row)


def get_second_lesson(day, week):
    row = get_row (day, "2", week)
    return print_lesson (row)
