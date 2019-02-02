import os

#  Set env var:
#    - Windows: setx <VAR NAME>=<VALUE>
#    - Linux: export <VAR NAME>=<VALUE>

TELEGRAM_API_TOKEN = os.environ.get('DONNU_BOT_TELEGRAM_API_TOKEN')
DB_USER_LOGIN = os.environ.get('DONNU_BOT_DB_USER_LOGIN')
DB_USER_PASSWORD = os.environ.get('DONNU_BOT_DB_USER_PASSWORD')
DB_HOST = os.environ.get('DONNU_BOT_DB_HOST')
DB_NAME = os.environ.get('DONNU_BOT_DB_NAME')


if not (TELEGRAM_API_TOKEN and DB_USER_LOGIN and DB_USER_PASSWORD and DB_HOST and DB_NAME):
    print('########################################')
    print('## Please, set next environ variable: ##')
    if not TELEGRAM_API_TOKEN:
        print('## - DONNU_BOT_TELEGRAM_API_TOKEN     ##')
    if not DB_USER_LOGIN:
        print('## - DONNU_BOT_DB_USER_LOGIN          ##')
    if not DB_USER_PASSWORD:
        print('## - DONNU_BOT_DB_USER_PASSWORD       ##')
    if not DB_HOST:
        print('## - DONNU_BOT_DB_HOST                ##')
    if not DB_NAME:
        print('## - DONNU_BOT_DB_NAME                ##')

    print('## See docs: https://git.io/fhPUh     ##')
    print('########################################')
    exit(-1)
