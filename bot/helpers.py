import datetime
from bot.config import DAYS_NAME, PAIR_TIME


def get_start_week(date):
    start = date - datetime.timedelta(days=date.isoweekday() - 1)
    return start


def get_day_name(date):
    return DAYS_NAME[date.isoweekday() - 1]


def get_pair_time(number):
    return '{} - {}'.format(*PAIR_TIME[number-1])
