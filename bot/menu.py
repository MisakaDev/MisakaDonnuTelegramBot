from aiogram import types
from db import Group


def default_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton("🗓 Розклад"))
    markup.row(types.KeyboardButton("🎮 Фічі"))
    markup.row(types.KeyboardButton("⚙️ Налаштування"), types.KeyboardButton("🔮 Допомога"))
    return markup


def schedule_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton("📕 На сьогодні"), types.KeyboardButton("📗 На завтра"))
    markup.row(types.KeyboardButton("📘 На цей тиждень"), types.KeyboardButton("📙 На наступний тиждень"))
    markup.row(types.KeyboardButton("📓 По даті"), types.KeyboardButton("📔 По тиждні"))
    markup.row(types.KeyboardButton("⬅️Назад"))
    return markup


def setting_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton("🏷 Змінити групу"))
    markup.row(types.KeyboardButton("⬅️Назад"))
    return markup


def back_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton("⬅️Назад"))
    return markup


def features_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton("🕗 Розклад пар"))
    markup.row(types.KeyboardButton("🧮 Статистика"))
    markup.row(types.KeyboardButton("⬅️Назад"))
    return markup


async def group_menu():
    markup = types.ReplyKeyboardMarkup()
    for group in await Group.get_all():
        markup.row(types.KeyboardButton(group.name))
    return markup
