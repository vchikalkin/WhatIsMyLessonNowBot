import datetime

import pytz

import sheets

dayofweek = datetime.datetime.today ().weekday ()
# dayofweek = 1
day_list = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
today = day_list[dayofweek]
# today = "Понедельник"
now_week = sheets.sheet.cell (23, 2).value
# now_week = "Числитель"

timezone = pytz.timezone ('Europe/Moscow')
hour = datetime.datetime.now (timezone).hour

day = today
week = now_week
