import keyboards
import main
import settings
import users


def login(user_id, message):
    if message.text in users.get_universities():
        settings.user_university = message.text
        university = settings.user_university
        main.send_keyboard(user_id, keyboards.GroupsKeyboard.answer, keyboards.GroupsKeyboard.get_groups(university))
    elif message.text in users.get_groups(settings.user_university):
        university = settings.user_university
        group = message.text
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        users.register(user_id, university, group, first_name, last_name)
        day = settings.get_day()
        main.send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)
    else:
        main.send_keyboard(user_id, keyboards.UniversitiesKeyboard.answer, keyboards.UniversitiesKeyboard.markup)
