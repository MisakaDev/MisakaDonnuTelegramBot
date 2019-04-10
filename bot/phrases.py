import datetime
import random

from bot.helpers import get_day_name, get_pair_time, get_pair_status
from db import Statistic


class Keyboard:
    SCHEDULE = '🗓 Розклад'
    SCHEDULE_TODAY = "📕 На сьогодні"
    SCHEDULE_TOMORROW = "📗 На завтра"
    SCHEDULE_CURRENT_WEEK = "📘 На цей тиждень"
    SCHEDULE_NEXT_WEEK = "📙 На наступний тиждень"
    SCHEDULE_BY_DAY = "📓 По даті"
    SCHEDULE_BY_WEEK = "📔 По тиждні"
    FEATURE = "🎮 Фічі"
    FEATURE_PAIR_INFO = '🕗 Розклад пар'
    FEATURE_STATISTIC = '🧮 Статистика'
    SETTING = "⚙️ Налаштування"
    SETTING_CHANGE_GROUP = "🏷 Змінити групу"
    BACK = "⬅️Назад"
    HELP = "🔮 Допомога"


start = lambda: random.choice(('Привіт. Для початку давай познайомимось.',))
start_error = lambda: random.choice(('Ми вже знайомі.', 'Я тебе пам\'ятаю.',))

course_select = lambda: random.choice(("Вибери курс на якому ти навчаєшся",))
course_unknown = lambda: random.choice(('В мене немає інформації про такий курс',))

group_select = lambda: random.choice(("Вибери свою группу", "В якій групі ти навчаєшся?"))
group_unknown = lambda: random.choice(('В мене немає інформації про таку группу',))
group_success = lambda: random.choice(('Добре, я тебе запам\'ятав',))

schedule = lambda: random.choice(("Що хочеш дізнатись?", "Що тобі підказати?"))
schedule_by_date = lambda: random.choice(("Введи день в форматі DD.MM.YYYY, і я покажу тобі розклад",))
schedule_by_week = lambda: random.choice(("Введи будь-який день в форматі DD.MM.YYYY, і я покажу розклад на цей "
                                          "тиждень",))

unknown_cmd = lambda: random.choice(("Що ти від мене хочеш? Я не розумію.",
                                     "Що ти таке написав? Я не можу це зрозуміти.",
                                     "Такої команди немає в моїй базі. Вибери щось із меню нижще."))

back = lambda: random.choice(('Чим можу допомогти?',))

setting = lambda: random.choice(('Що бажаєш змінити?',))

user_help = lambda: "Ого, все настільки погано що тобі потрібна допомога? " \
                    "Бот може лагати/зависати/помилятись, але все ж інколи працює правильно. " \
                    "Знайшов баг? Пиши (c) @MisakaDev\n" \
                    "Потрібен соус? Тримай: https://github.com/MisakaDev/MisakaDonnuTelegramBot"

schedule_for = lambda: random.choice(("Ось розклад на: ", "Тримай розклад на: "))

free_day = lambda: random.choice(("В цей день пар не буде",))

format_parse_error = lambda: random.choice(("Я не розумію що тут написанно, спробуй ще раз",))

features = lambda: random.choice(("Ось що я ще вмію",))

user_has_no_group = lambda: random.choice(("Для початку вкажи свою групу в налаштуваннях",))

admin_update_schedule_user_message = lambda: random.choice(("Бот оновлює данні. Спробуй ще раз через хвилину",))
admin_update_schedule_success = lambda: random.choice(("Розклад успішно оновлено!",))
admin_update_schedule_error_parse = lambda error: random.choice(("Помилка при оновлені: " + str(error),))
admin_update_schedule_error_bad_file = lambda: random.choice(("Я не розумію що це за файл. Надішли мені таблицю!",))
admin_update_schedule_error_not_admin = lambda: random.choice(("Ей, в тебе немає прав!",))


def render_pair_info():
    return "\n".join(["{} {} пара: {}".format(
        get_pair_status(number),
        number,
        get_pair_time(number)
    ) for number in range(1, 9)],)


def render_user_info(user, group):
    if group:
        return "Наскільки я пам'ятаю твоя група: " + group.name + '\n'
    else:
        return "Ти ще не вказав свою групу\n"


def render_schedule_for_date(schedule_info, date, header=True):
    reply = "{}{} {:02}.{:02}.{:02}:\n".format(schedule_for() if header else "", get_day_name(date), date.day,
                                               date.month, date.year)
    if not schedule_info:
        reply += free_day() + '\n'
    for pair in schedule_info:
        reply += "▫ #{} [{}] - {}\n".format(pair.pair_number, get_pair_time(pair.pair_number), pair.information)
    return reply


def render_schedule_for_week(schedule_info):
    start_day = list(schedule_info.keys())[0]
    end_day = list(schedule_info.keys())[len(schedule_info) - 1]
    reply = "{} {:02}.{:02}.{:02}-{:02}.{:02}.{:02}:\n".format(schedule_for(),
                                                               start_day.day, start_day.month, start_day.year,
                                                               end_day.day, end_day.month, end_day.year)
    for day, schedule_data in schedule_info.items():
        reply += "==========\n" + render_schedule_for_date(schedule_data, day, header=False)
    return reply


async def render_statistics():
    now = datetime.datetime.now()

    count_by_hours = await Statistic.count_by_date_interval(now - datetime.timedelta(hours=1), now)
    count_by_day = await Statistic.count_by_date_interval(now - datetime.timedelta(days=1), now)
    count_by_month = await Statistic.count_by_date_interval(now - datetime.timedelta(days=30), now)

    count = "🔄 Оброблено повідомлень: \n \tЗа годину: {} \n \tЗа день: {} \n \tЗа місяць: {}".format(
        count_by_hours,
        count_by_day,
        count_by_month
    )

    user_by_hours = await Statistic.active_users_by_date_interval(now - datetime.timedelta(hours=1), now)
    user_by_day = await Statistic.active_users_by_date_interval(now - datetime.timedelta(days=1), now)
    user_by_month = await Statistic.active_users_by_date_interval(now - datetime.timedelta(days=30), now)

    user = "🚻 Активних користувачів: \n \tЗа годину: {} \n \tЗа день: {} \n \tЗа місяць: {}".format(
        user_by_hours,
        user_by_day,
        user_by_month
    )

    top_message = (await Statistic.message_rating())[:3]

    top = "🆙 Найпопулярніший запит: \n \t{}".format(
        "\n \t".join(['{} - {}'.format(count, message) for message, count in top_message])
    )

    return "{}\n{}\n{}".format(count, user, top)
