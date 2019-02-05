from aiogram import types

from db import Group
from .phrases import Keyboard


def default_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton(Keyboard.SCHEDULE))
    markup.row(types.KeyboardButton(Keyboard.FEATURE))
    markup.row(types.KeyboardButton(Keyboard.SETTING), types.KeyboardButton(Keyboard.HELP))
    return markup


def schedule_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton(Keyboard.SCHEDULE_TODAY), types.KeyboardButton(Keyboard.SCHEDULE_TOMORROW))
    markup.row(types.KeyboardButton(Keyboard.SCHEDULE_CURRENT_WEEK), types.KeyboardButton(Keyboard.SCHEDULE_NEXT_WEEK))
    markup.row(types.KeyboardButton(Keyboard.SCHEDULE_BY_DAY), types.KeyboardButton(Keyboard.SCHEDULE_BY_WEEK))
    markup.row(types.KeyboardButton(Keyboard.BACK))
    return markup


def setting_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton(Keyboard.SETTING_CHANGE_GROUP))
    markup.row(types.KeyboardButton(Keyboard.BACK))
    return markup


def back_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton(Keyboard.BACK))
    return markup


def features_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton(Keyboard.FEATURE_PAIR_INFO))
    markup.row(types.KeyboardButton(Keyboard.FEATURE_STATISTIC))
    markup.row(types.KeyboardButton(Keyboard.BACK))
    return markup


async def course_menu():
    markup = types.ReplyKeyboardMarkup()
    for group in await Group.get_course_list():
        markup.row(types.KeyboardButton(group.course))
    markup.row(types.KeyboardButton(Keyboard.BACK))
    return markup


async def group_menu(course):
    markup = types.ReplyKeyboardMarkup()
    for group in await Group.get_by_course(course):
        markup.row(types.KeyboardButton(group.name))
    markup.row(types.KeyboardButton(Keyboard.BACK))
    return markup
