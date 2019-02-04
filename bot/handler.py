from . import dp, bot
from aiogram import types

from db import User, Group
import datetime

import bot.phrases as phrases
import bot.menu as menu
import bot.helpers as helpers

from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message, state: FSMContext):
    user = await User.get_or_create(telegram_id=message.from_user.id)
    if user.group_id:
        return await bot.send_message(message.chat.id, phrases.start_error())

    message.text = '🏷 Змінити групу'
    await bot.send_message(message.chat.id, phrases.start())

    await setting_change_group(message, state)


@dp.message_handler(lambda message: message.text == '⬅️Назад')
async def back(message):
    await bot.send_message(message.chat.id, phrases.back(), reply_markup=menu.default_menu())


@dp.message_handler(lambda message: message.text == '🗓 Розклад')
async def schedule(message):
    user = await User.get_or_create(telegram_id=message.from_user.id)
    if not user.group_id:
        return await bot.send_message(message.chat.id, phrases.user_has_no_group(), reply_markup=menu.default_menu())
    await bot.send_message(message.chat.id, phrases.schedule(), reply_markup=menu.schedule_menu())


@dp.message_handler(lambda message: message.text == '📕 На сьогодні')
async def schedule_today(message):
    user = await User.get_or_create(telegram_id=message.from_user.id)
    schedule_for_date = await user.get_schedule_by_day(message.date)
    await bot.send_message(message.chat.id, phrases.render_schedule_for_date(schedule_for_date, message.date))


@dp.message_handler(lambda message: message.text == '📗 На завтра')
async def schedule_tomorrow(message):
    user = await User.get_or_create(telegram_id=message.from_user.id)
    tomorrow_date = message.date + datetime.timedelta(days=1)
    schedule_for_date = await user.get_schedule_by_day(tomorrow_date)
    await bot.send_message(message.chat.id, phrases.render_schedule_for_date(schedule_for_date, tomorrow_date))


@dp.message_handler(lambda message: message.text == '📘 На цей тиждень')
async def schedule_current_week(message):
    user = await User.get_or_create(telegram_id=message.from_user.id)
    week_start = helpers.get_start_week(message.date)
    week_days = [week_start + datetime.timedelta(days=delta) for delta in range(6)]
    week_schedule = {day: await user.get_schedule_by_day(day) for day in week_days}
    await bot.send_message(message.chat.id, phrases.render_schedule_for_week(week_schedule))


@dp.message_handler(lambda message: message.text == '📙 На наступний тиждень')
async def schedule_next_week(message):
    user = await User.get_or_create(telegram_id=message.from_user.id)
    message_date = message.date + datetime.timedelta(days=7)
    week_start = helpers.get_start_week(message_date)
    week_days = [week_start + datetime.timedelta(days=delta) for delta in range(6)]
    week_schedule = {day: await user.get_schedule_by_day(day) for day in week_days}
    await bot.send_message(message.chat.id, phrases.render_schedule_for_week(week_schedule))


@dp.message_handler(lambda message: message.text == '📓 По даті')
@dp.message_handler(state='schedule_by_day')
async def schedule_by_day(message, state: FSMContext):
    if message.text == "⬅️Назад":
        await state.finish()
        return await schedule(message)
    user = await User.get_or_create(telegram_id=message.from_user.id)
    if message.text != '📓 По даті':
        try:
            message_date = datetime.datetime.strptime(message.text, '%d.%m.%Y').date()
            schedule_for_date = await user.get_schedule_by_day(message_date)
            await bot.send_message(message.chat.id, phrases.render_schedule_for_date(schedule_for_date, message_date))
        except:
            await bot.send_message(message.chat.id, phrases.format_parse_error())
    await bot.send_message(message.chat.id, phrases.schedule_by_date(), reply_markup=menu.back_menu())
    await state.set_state('schedule_by_day')


@dp.message_handler(lambda message: message.text == '📔 По тиждні')
@dp.message_handler(state='schedule_by_week')
async def schedule_by_week(message, state: FSMContext):
    if message.text == "⬅️Назад":
        await state.finish()
        return await schedule(message)
    user = await User.get_or_create(telegram_id=message.from_user.id)
    if message.text != '📔 По тиждні':
        try:
            message_date = datetime.datetime.strptime(message.text, '%d.%m.%Y').date()
            week_start = helpers.get_start_week(message_date)
            week_days = [week_start + datetime.timedelta(days=delta) for delta in range(6)]
            week_schedule = {day: await user.get_schedule_by_day(day) for day in week_days}
            await bot.send_message(message.chat.id, phrases.render_schedule_for_week(week_schedule))
        except:
            await bot.send_message(message.chat.id, phrases.format_parse_error())
    await bot.send_message(message.chat.id, phrases.schedule_by_week(), reply_markup=menu.back_menu())
    await state.set_state('schedule_by_week')


@dp.message_handler(lambda message: message.text == '⚙️ Налаштування')
async def setting(message):
    user = await User.get_or_create(message.from_user.id)
    group = await Group.get_by_id(user.group_id)
    await bot.send_message(message.chat.id, phrases.render_user_info(user, group) + phrases.setting(),
                           reply_markup=menu.setting_menu())


@dp.message_handler(lambda message: message.text == '🏷 Змінити групу')
async def setting_change_group(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, phrases.course_select(), reply_markup=await menu.course_menu())
    await state.set_state('change_group_select_course')


@dp.message_handler(state='change_group_select_course')
async def change_group_select_course(message: types.Message, state: FSMContext):
    if message.text == "⬅️Назад":
        await state.finish()
        return await setting(message)

    group_count = len(await Group.get_by_course(message.text))

    if not group_count:
        await bot.send_message(message.chat.id, phrases.course_unknown())
        await setting_change_group(message, state)
        return
    save = {'course': str(message.text)}

    await state.set_data(save)
    await state.set_state('change_group_select_group')
    await bot.send_message(message.chat.id, phrases.group_select(), reply_markup=await menu.group_menu(message.text))


@dp.message_handler(state='change_group_select_group')
async def change_group_select_group(message: types.Message, state: FSMContext):
    if message.text == "⬅️Назад":
        await state.set_state('change_group_select_course')
        return await setting_change_group(message, state)
    save = await state.get_data()
    course = save.get('course')
    group = await Group.get(message.text, course)

    if not group:
        await bot.send_message(message.chat.id, phrases.group_unknown())
        message.text = course
        await change_group_select_course(message, state)
        return

    user = await User.get_or_create(telegram_id=message.from_user.id)
    await user.set_group(group.id)
    await bot.send_message(message.chat.id, phrases.group_success(), reply_markup=menu.default_menu())
    await state.finish()


@dp.message_handler(lambda message: message.text == '🎮 Фічі')
async def features(message):
    await bot.send_message(message.chat.id, phrases.features(), reply_markup=menu.features_menu())


@dp.message_handler(lambda message: message.text == '🕗 Розклад пар')
async def features_pair_info(message):
    await bot.send_message(message.chat.id, phrases.render_pair_info(), reply_markup=menu.features_menu())


@dp.message_handler(lambda message: message.text == '🔮 Допомога')
async def user_help(message):
    await bot.send_message(message.chat.id, phrases.user_help(), reply_markup=menu.default_menu())


@dp.message_handler(lambda message: message.text == '🧮 Статистика')
async def statistic(message):
    await bot.send_message(message.chat.id, await phrases.render_statistics(), reply_markup=menu.features_menu())


@dp.message_handler()
async def unknown(message):
    await bot.send_message(message.chat.id, phrases.unknown_cmd(), reply_markup=menu.default_menu())
