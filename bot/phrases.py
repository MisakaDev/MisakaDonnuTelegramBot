import random
from bot.helpers import get_day_name, get_pair_time, get_pair_status

start = lambda: random.choice(('Привіт. Для початку давай познайомимось.',))
start_error = lambda: random.choice(('Ми вже знайомі.', 'Я тебе пам\'ятаю.',))

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
