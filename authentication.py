import keyboards
import main
import settings
import user
import users

user = user.User()


def login(user_id, message):
    if message.text in users.get_universities():
        user.university = message.text
        university = user.university
        main.send_keyboard(user_id, keyboards.GroupsKeyboard.answer, keyboards.GroupsKeyboard.get_groups(university))

    elif message.text in users.get_groups(user.university):
        university = user.university
        group = message.text
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        users.register(user_id, university, group, first_name, last_name)
        day = settings.get_day()
        main.send_keyboard(user_id, keyboards.DaysKeyboard.get_answer(day), keyboards.DaysKeyboard.markup)

    else:
        main.send_keyboard(user_id, keyboards.UniversitiesKeyboard.answer, keyboards.UniversitiesKeyboard.markup)
