# MisakaDonnuTelegramBot

MisakaDonnuTelegramBot - це бот телеграм який допомагає дізнатись розклад.

## Встановлення

Перед використанням бота встановіть наступні зміні оточення:
```
Для Windows: setx <VAR NAME>=<VALUE>
Для Linux: export <VAR NAME>=<VALUE>
```

```
DONNU_BOT_TELEGRAM_API_TOKEN - Токен Вашого бота
DONNU_BOT_DB_HOST - Хост бази данних PostgreSQL
DONNU_BOT_DB_NAME - Ім'я бази данних
DONNU_BOT_DB_USER_LOGIN - Логін користувача 
DONNU_BOT_DB_USER_PASSWORD - Пароль користувача
```

Клонуйне проект і запустіть:
```bash
git clone https://github.com/MisakaDev/MisakaDonnuTelegramBot
cd MisakaDonnuTelegramBot
pip install -r requirements.txt
python __init__.py
```

## Використання

У папці parsers Ви можете знайти приклади парсерів xlsx файлів з розкладом. 
Перед використання бота необхідно наповнити базу данних одним з таких парсерів.

## Інтерфейс
![image](https://user-images.githubusercontent.com/31675199/54159525-d5b79d00-4455-11e9-9661-065ebe9c53b0.png)
![image](https://user-images.githubusercontent.com/31675199/54159564-eec04e00-4455-11e9-96bd-d9718b7a639f.png)
![image](https://user-images.githubusercontent.com/31675199/54159833-a2294280-4456-11e9-9004-08e35b89c8a7.png)

## Contributing
Pull-запити вітаються. Для значних змін, спочатку відкрийте issue, щоб обговорити те, що ви хотіли б змінити.


## License
[GNU General Public License v3.0](https://github.com/MisakaDev/MisakaDonnuTelegramBot/blob/master/LICENSE)
