# Проект — exchange_rate_telegram_bot

Exchange_rate_telegram_bot — это проект, который реализует telegram-bot для конвертации валют,
введенных от пользователя. Данный скрипт использует API для получения валют и сохраняет их в json-файл.
В коде используются библиотеки: `json`, `requests`, `datetime`, `telebot`


# Команды бота:

- `/start` — приветственное сообщение
- `/help` — справка
- `/convert` — получение курса валют
- `/get_requests` — совершенные операции по конвертации валют
- `/get_symbols` — полный список аббревиатур символов валют, доступных для конвертации


# Клонирование репозитория

В проекте для управления зависимостями используется [poetry](https://python-poetry.org/). </br>
Выполните в консоли: </br>

Для Windows: </br>
```
git clone git@github.com:DmitriiParfenov/exchange_rate_telegram_bot.git
python -m venv venv
venv\Scripts\activate
pip install poetry
poetry install
```

Для Linux: </br>
```
git clone git@github.com:DmitriiParfenov/exchange_rate_telegram_bot.git
cd exchange_rate_telegram_bot
python3 -m venv venv
source venv/bin/activate
curl -sSL https://install.python-poetry.org | python3
poetry install
```

# Запуск

- Получите ключ API для получения курсов валют на сайте [apilayer.com](https://apilayer.com/marketplace/exchangerates_data-api).
- Установите ключ API в переменную окружения: `EXCHANGE_RATE_API_KEY`.
- Создайте свой телеграм-бот с помошью бота [BotFather](https://t.me/botfather) через команду `/newbot`.
- Получите ключ API от `BotFather` после создания своего телеграм-бота.
- Установите ключ API в переменную окружения: `TELEGRAM_API_KEY`.
- Запустите скрипт.


# Использование бота

1. Зайдите в свой телеграм-бот.
2. Введите `/convert`.
3. Бот спросит, приступаем ли мы к конвертации или нет: </br>
   - `да` или `Да` для старта конвертации, `нет` или `Нет` — для отмены конвертации.
4. Далее бот последовательно запросит у пользователя с какой валюты и по отношению к какой валюте выполнить конвертацию.
   - необходимо вводить  аббревиатуры валют на английском языке, например, российские рубли — `RUB` или `rub`.
5. Бот получит текущий курс валюты от API и выведет его.
6. Курс валюты и дата получения будут сохранены в json файле `currency_rates.json`.