import gspread
from oauth2client.service_account import ServiceAccountCredentials

import settings

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name ('googleauth.json', scope)
client = gspread.authorize (creds)

sheet = client.open ("Sheet1").sheet1


def get_row(day, num, week):
    days = sheet.findall (day)
    for d in days:
        row = d.row
        if sheet.cell (row, 2).value == week:
            if sheet.cell (row, 3).value == num:
                return row


def get_aud_force(num):
    days = sheet.findall (settings.today)
    for d in days:
        row = d.row
        if sheet.cell (row, 2).value == settings.now_week:
            if sheet.cell (row, 3).value == num:
                return "Тебе в " + sheet.cell (row, 5).value + ". Там тебя ждет " + sheet.cell (row, 8).value


def print_lesson(row):
    return "Время: " + sheet.cell (row, 4).value + "\n" \
                                                   "Ауд.: " + sheet.cell (row, 5).value + "\n" + \
           "Тип: " + sheet.cell (row, 6).value + "\n" + \
           "Назв.: " + sheet.cell (row, 7).value + "\n" + \
           "Препод: " + sheet.cell (row, 8).value


def get_first_lesson(day, week):
    row = get_row (day, "1", week)
    return print_lesson (row)


def get_second_lesson(day, week):
    row = get_row (day, "2", week)
    return print_lesson (row)
