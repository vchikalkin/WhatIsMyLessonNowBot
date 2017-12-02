import telebot

import settings
import users


class DaysKeyboard:
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row('Понедельник', 'Вторник')
    markup.row('Среда', 'Четверг')
    markup.row('Пятница')
    markup.row('КУДА МНЕ ИДТИ?')
    markup.row('Настройки')

    @staticmethod
    def get_answer(day):
        answer = "Выбери день...\n_(Сегодня {0}, если что)_".format(day)
        return answer


class WeekKeyboard:
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row('Числитель', 'Знаменатель')
    markup.row('Назад')

    @staticmethod
    def get_week(week):
        answer = "Выбери неделю...\n_(Сейчас {0}, если что)_".format(week)
        return answer


class UniversitiesKeyboard:
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    for i in users.get_universities():
        markup.row(i)
    answer = "Выбери свой ВУЗ..."


class GroupsKeyboard:
    @staticmethod
    def get_groups(university):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for i in users.get_groups(university):
            markup.row(i)
        return markup

    answer = "Выбери свою группу..."


class SettingsKeyboard:
    @staticmethod
    def get_markup(user_id):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Сменить группу')
        if user_id == settings.admin_id:
            markup.row('Выбрать неделю')
        markup.row('Назад')
        return markup

    answer = "Настройки"


class AdminKeyboard:
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row('/Числитель', '/Знаменатель')
    markup.row('Назад')
    answer = "Установлен параметр '" + settings.get_week() + "'"


class HideKeyboard():
    hide_markup = telebot.types.ReplyKeyboardRemove()
