import groups
import keyboards
import main
import settings
import user
import users

current_user = user.User()


def login(user_id, message):
    if message.text in groups.get_universities():
        current_user.university = groups.get_university_eng(message.text)
        university = current_user.university
        main.send_keyboard(user_id,
                           keyboards.GroupsKeyboard.answer,
                           keyboards.GroupsKeyboard.get_groups(university))

    elif message.text in groups.get_groups(current_user.university):
        university = current_user.university
        group = groups.get_group_eng(message.text)
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        users.register(user_id,
                       university,
                       group,
                       first_name,
                       last_name)
        day = settings.get_current_day()
        main.send_keyboard(user_id,
                           keyboards.DaysKeyboard.get_answer(day),
                           keyboards.DaysKeyboard.markup)

    else:
        main.send_keyboard(user_id,
                           keyboards.UniversitiesKeyboard.answer,
                           keyboards.UniversitiesKeyboard.markup)
